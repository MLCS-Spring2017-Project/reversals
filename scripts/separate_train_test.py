import os
import shutil

src = "ngrams/train"
dest = "ngrams/test"

for folder in os.listdir(src):

    count = len(os.listdir(src + "/" + folder)) / 10

    for file in os.listdir(src + "/" + folder):

        if count < 1:
            break
        if not os.path.exists(dest + "/" + folder):
            os.makedirs(dest + "/" + folder)

        shutil.move(src + "/" + folder + "/" + file, dest + "/" + folder + "/" + file)
        count -= 1
