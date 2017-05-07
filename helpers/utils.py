import os
import csv

from collections import Counter


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


def trim_dic(dic):
    # total = len(dic[row])
    # current = 0
    # for i in dic:
    #     current += dic[i]
    #
    # average = (1.0 * current) / total
    #
    # for i in dic.iteritems():
    #     if dic[i] < average:
    #         dic.pop(i)
    total = len(dic.keys())
    final = dic.most_common(int(total / 8)) + dic.most_common()[- int(total / 8):]
    return dict(final)


def read_file_to_dict(target_path, trim=True):
    reader = csv.reader(open(target_path))

    dic = Counter()
    for row in reader:
        dic[row[0]] = int(row[1])

    if trim:
        dic = trim_dic(dic)

    return dic


def text_from_district_file(path):
    with open(path, 'r') as f:
        text = f.read()
        text = text.lower().split("judge", maxsplit=1)
        if len(text) == 2:
            text = text[1]
        else:
            text = "judge".join(text)
    return text
