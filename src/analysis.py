from utils import *
import numpy as np


def vowel_space_diphthong_extractor(acoustics_values):
    """
    deal with diphthong
    """
    return acoustics_values[0], acoustics_values[1]


def vowel_space_avg_extractor(acoustics_values):
    """
    deal with single vowel
    """
    return sum(acoustics_values) / 3


def duration_data():
    duration = {}
    for row in read_data():
        phone = row["Phone"]
        if not is_diphthong(phone):
            if phone not in duration:
                duration[phone] = []
            duration[phone].append(float(row["Duration (s)"]))
    for phone, d in duration.items():
        num_ob = len(d)
        avg_duration = sum(d) / num_ob
        stdev = np.std(d)
        print("Phoneme: {}; # of observations: {}; mean duration: {}; stdev: {}".format(phone, num_ob, avg_duration, stdev))


def vowel_space_data():
    for row in read_data():
        phone = row["Phone"]
        if is_diphthong(phone):
            phone1, phone2 = phone[0], phone[1]
            f1_values = extract_acoustics(row, "F1", vowel_space_diphthong_extractor)
            f2_values = extract_acoustics(row, "F2", vowel_space_diphthong_extractor)
            yield phone1, f1_values[0], f2_values[0]
            yield phone2, f1_values[1], f2_values[1]
        else:
            yield phone, \
                  extract_acoustics(row, "F1", vowel_space_avg_extractor), \
                  extract_acoustics(row, "F2", vowel_space_avg_extractor)


def plot_vowel_space(log_scale=False):
    import matplotlib.pyplot as plt
    import pylab

    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    plt.xlabel("F2")
    plt.ylabel("F1")
    f2_data = []
    f1_data = []
    phones = []
    for phoneme, f1, f2 in vowel_space_data():
        f2_data.append(f2)
        f1_data.append(f1)
        phones.append(phoneme)

    phone_set = sorted(list(set(phones)))
    print("different vowels: ", phone_set)
    phone_dict = {p: i for i, p in enumerate(phone_set)}
    colors = [phone_dict[phone] for phone in phones]

    plt.scatter(f2_data, f1_data, c=colors, cmap=pylab.cm.cool)

    for i, phone in enumerate(phones):
        plt.annotate(phone, (f2_data[i], f1_data[i]))

    if log_scale:
        plt.yscale('log')
        plt.xscale('log')
    plt.show()


def diphthong_data():
    for row in read_data():
        phone = row["Phone"]
        if is_diphthong(phone):
            f1_values = extract_acoustics(row, "F1", vowel_space_diphthong_extractor)
            f2_values = extract_acoustics(row, "F2", vowel_space_diphthong_extractor)
            yield phone, (f1_values[0], f2_values[0]), (f1_values[1], f2_values[1])


def plot_diphthong_movement():
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    import matplotlib.cm as cm

    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    plt.xlabel("F2")
    plt.ylabel("F1")
    vec_start_x = []
    vec_start_y = []
    vec_comp_x = []
    vec_comp_y = []
    phones = []

    for phone, first_point, second_point in diphthong_data():
        phones.append(phone)
        vec_start_x.append(first_point[1])
        vec_start_y.append(first_point[0])
        vec_comp_x.append(second_point[1] - first_point[1])
        vec_comp_y.append(second_point[0] - first_point[0])

    phone_set = sorted(list(set(phones)))
    phone_dict = {p: i for i, p in enumerate(phone_set)}
    colors = [phone_dict[p] for p in phones]
    norm = Normalize()
    norm.autoscale(colors)
    colormap = cm.cool

    plt.quiver(vec_start_x, vec_start_y, vec_comp_x, vec_comp_y, color=colormap(norm(colors)), angles='xy', scale_units='xy', scale=1)

    for i, phone in enumerate(phones):
        plt.annotate(phone, (vec_start_x[i] + 0.5 * vec_comp_x[i], vec_start_y[i] + 0.5 * vec_comp_y[i]))

    plt.show()


if __name__ == "__main__":
    duration_data()
    # plot_vowel_space()
    plot_diphthong_movement()
