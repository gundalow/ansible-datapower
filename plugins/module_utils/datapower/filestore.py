import os
import random
import string
import posixpath
from difflib import context_diff
from ansible_collections.community.datapower.plugins.module_utils.datapower.files import (
    LocalFile
)


def copy_file_to_tmp_directory(module, tmpdir, src, dest, content):
    random_string = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    tmp_path = os.path.join(tmpdir, random_string, dest.lstrip('/'))
    if src and os.path.isfile(src):
        os.makedirs(os.path.split(tmp_path)[0])
        module.preserved_copy(src, tmp_path)
        return LocalFile(path=tmp_path)
    elif not src and content:
        # Create file from content
        return LocalFile(path=tmp_path, content=content)
    

def get_file_diff(from_local_file, to_local_file, dest, state):
    if state == 'present':
        if from_local_file and to_local_file:
            return list(context_diff(
                a=from_local_file.get_lines(),
                b=to_local_file.get_lines(),
                fromfile=os.path.join('before', dest),
                tofile=os.path.join('after', dest),
                n=3
            ))
        elif to_local_file and from_local_file is None:
            return {
                'before': None,
                'after': dest
            }
    else:
        if from_local_file:
            return {
                'before': dest,
                'after': None
            }
        else:
            return {'before': None, 'after': None}


def get_files_from_filestore(filestore):
    if isinstance(filestore['filestore']['location']['file'], dict):
        return [filestore['filestore']['location']['file']['href']]
    else:
        return [file['href'] for file in filestore['filestore']['location']['file']]


def get_request_func(req, before_file, after_file, state):
    if state == 'present':
        if before_file is None:
            return req.post
        else:
            if before_file != after_file:
                return req.put
            else:
                return None
    else:
        if before_file is None:
            return None
        else:
            return req.delete


def get_parent_dir(path):
    # Get the parent directory
    return posixpath.split(path)[0]