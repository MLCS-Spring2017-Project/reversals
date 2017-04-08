import os
import shutil

src = ""
dest = ""

for folder in os.listdir():

    count = len(os.listdir(folder)) / 10

    for file in os.listdir(folder):

        if count < 1:
            break

        shutil.move(src, dest)
        count -= 1
