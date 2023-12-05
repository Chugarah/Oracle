import os


def get_files_info(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield {
                'file_id': os.urandom(12).hex(),  # generate a random file id
                # get file name without extension
                'file_name': os.path.splitext(file)[0],
                # get file extension
                'file_extension': os.path.splitext(file)[1],
                # get file size
                'file_size': os.path.getsize(os.path.join(root, file)),
                # get absolute file path
                'file_location': os.path.join(root, file)
            }


def check_file_exists(file_path):
    return os.path.exists(file_path)
