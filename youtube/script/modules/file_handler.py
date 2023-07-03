import os


# The `FolderScanner` class provides a static method `scan_folder` that scans a given folder for files
# with specified extensions and returns a list of tuples containing the file path, current folder, and
# file name without extension.
class FolderScanner:
    @staticmethod
    def scan_folder(folder, extensions):
        wave_list = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    webm_path = os.path.join(root, file)
                    normalized_path = os.path.normpath(webm_path)
                    current_folder = os.path.dirname(normalized_path)
                    file_name_without_extension = os.path.splitext(
                        os.path.basename(normalized_path))[0]

                    # Check if the file exists
                    if os.path.exists(normalized_path):
                        wave_list.append(
                            (normalized_path, current_folder, file_name_without_extension))
        return wave_list
