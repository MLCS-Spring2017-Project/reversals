"""
Oversamples a directory to make the count of affirm and reverse equal
Usage: `python oversampler.py <path/to/directory>`
"""
import sys
import shutil
import glob
import os
from random import randint
import uuid


def oversample(data_folder):
    path = os.path.join(data_folder, "**", "*.txt")
    texts = glob.glob(path, recursive=True)
    data = {"Affirmed": [], "Reversed": []}

    for text in texts:
        label_path = text[:-4] + ".lab"

        with open(label_path, "r") as f:
            label = f.read().strip()
        data[label].append(text)

    reverse_count = len(data["Reversed"])
    affirm_count = len(data["Affirmed"])
    print(reverse_count, affirm_count)

    if reverse_count < affirm_count:
        for i in range(0, affirm_count - reverse_count):
            rand = randint(0, reverse_count)
            text = data["Reversed"][rand]
            uid = str(uuid.uuid4().hex)

            # Copy text
            path = text.split('/')[:-1]
            path.append(uid + ".txt")
            path = os.path.join(*path)
            path = "/" + path
            shutil.copyfile(text, path)

            # Copy lab
            path = path[:-4] + ".lab"
            text = text[:-4] + ".lab"
            shutil.copyfile(text, path)


if __name__ == '__main__':
    oversample(sys.argv[1])
