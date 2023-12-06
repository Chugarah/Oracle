import os


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

                    if os.path.exists(normalized_path):
                        wave_list.append(
                            (normalized_path, current_folder, file_name_without_extension))

        return wave_list

    @staticmethod
    def get_new_ids(folder, extensions, downloaded_ids):
        scanned_ids = set()
        for root, dirs, files in os.walk(folder):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_id = os.path.splitext(os.path.basename(file))[0]
                    if file_id not in downloaded_ids:
                        scanned_ids.add(file_id)
        return scanned_ids
