import os
import csv


def save_dict_to_file(target_path, dict_to_save):
    """
    Saves the provided dictionary into the specified path
    """
    if not os.path.exists(os.path.dirname(target_path)):
        try:
            os.makedirs(os.path.dirname(target_path))
        except OSError as exc:
            # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    writer = csv.writer(open(target_path, 'w'))

    for key, value in dict_to_save.items():
        try:
            writer.writerow([key, value])
        except Exception as e:
            print(str(e))
            pass
