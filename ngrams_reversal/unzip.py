import helper
import os
import zipfile


def get_name_without_extension(name):
    """
    Returns the filename without extension
    """

    return ''.join(os.path.basename(name).split('.')[:-1])


def unzip_file(zip_file, target_dir=None):
    """
    Unzips the 'zip_file' into the 'target_dir'
    If target is not specified, filename will be used
    Returns the name of the directory the contents are zipped into
    """

    if target_dir is None:
        target_dir = get_name_without_extension(zip_file)
        
    z = zipfile.ZipFile(zip_file)
    z.extractall(target_dir)
    z.close()

    return target_dir

# unzip_file('./1890.zip')

for x in helper.get_files('.'):

    if x.endswith('.zip'):
        print(x)
        unzip_file(x)
        os.remove(x)

    