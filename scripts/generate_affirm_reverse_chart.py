import matplotlib.pyplot as plt
import glob
import os
import sys
import pickle


def check_case_status(case):
    if case.empty:
        return False
    elif case['Affirmed'].tolist()[0] == 0.0 \
            and case['Reversed'].tolist()[0] == 0.0:
        return False
    elif case['Affirmed'].tolist()[0] == 1.0:
        status = "Affirmed"
    else:
        status = "Reversed"
    return status


def main():
    files = glob.glob(os.path.join(sys.argv[1], "**", "*.txt"))
    affirm_reverse_path = os.path.abspath("district_affirm_reverse.pkl")
    dic = pickle.load(open(affirm_reverse_path, "rb"))

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Affirmed', 'Reversed'
    sizes = [0, 0]
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    for fname in files:
        caseid = fname.split("/")[-1][:-4]
        case = dic.loc[dic['caseid'] == caseid]
        status = check_case_status(case)
        if not status:
            continue

        if status == 'Affirmed':
            sizes[0] += 1
        elif status == 'Reversed':
            sizes[1] += 1
    plt.rcParams['font.size'] = 16.0

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig("affirm_reverse_partition.png", transparent=True)


if __name__ == '__main__':
    main()
