#!/usr/bin/env python3
"""Script to plot graphs from csv
"""

import os
import pandas
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

def plot_vs_bar(csv_fp):
    db = pandas.read_csv(csv_fp)
    dates_list = db["date"].array
    classical_list = db["classical"].array
    ml_list = db["ML-based"].array

    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(dates_list))  # the label location
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    width = 0.2  # the width of the bars
    multiplier = 0
    font_size = 22

    for type_i in range(2):
        # puh, im sure there is a better way to do this
        if type_i == 1:
            heights = classical_list
            tag_str = "classical method"
        elif type_i == 0:
            heights = ml_list
            tag_str = "image-based pipeline"
        else:
            # this should throw an actual error
            print("Cannot print bar: error in type of bar! Only two types of bars available")
            break

        offset = width * multiplier
        rects = ax.bar(x+offset,  heights, width, label=tag_str)
        ax.bar_label(rects, padding=3, fontsize=12, fmt="%.0f")

        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of individuals per meter squared, per hour', fontsize=font_size)
    ax.set_title('Number of individuals per meter squared, per hour by evaluation method')
    ax.set_xticks(x + width, [x for x in dates_list], fontsize=font_size)
    ax.legend(loc='upper right')

    plt.savefig(f"classic_vs_ml.png")
    plt.close()
    # import pdb; pdb.set_trace()

def plot_by_treatment(csv_fp):
    db = pandas.read_csv(csv_fp)
    dates_list = db["treatment"].array
    classical_list = db["classical"].array
    ml_list = db["ML-based"].array

    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(dates_list))  # the label location
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    width = 0.2  # the width of the bars
    multiplier = 0
    font_size = 22

    for type_i in range(2):
        # puh, im sure there is a better way to do this
        if type_i == 1:
            heights = classical_list
            tag_str = "classical method"
        elif type_i == 0:
            heights = ml_list
            tag_str = "image-based pipeline"
        else:
            # this should throw an actual error
            print("Cannot print bar: error in type of bar! Only two types of bars available")
            break

        offset = width * multiplier
        rects = ax.bar(x+offset,  heights, width, label=tag_str)
        ax.bar_label(rects, padding=3, fontsize=12, fmt="%.0f")

        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of individuals ($\mathregular{h^{-1}m^{-2}}$)', fontsize=font_size)
    # ax.set_title('Number of individuals ($\mathregular{h^{-1}m^{-2}}$) per treatment\n by evaluation method')
    ax.set_xticks(x + width, [x for x in dates_list], fontsize=font_size)
    ax.legend(loc='upper right')

    plt.savefig(f"classic_vs_ml_by_treatment_notitle.png")
    # plt.savefig(f"classic_vs_ml_by_treatment.png")
    plt.close()

    # import pdb; pdb.set_trace()
    

if __name__ == "__main__":
    csv_dir = "../data_csvs"
    # plot_vs_bar(os.path.join(csv_dir, "classic_vs_ml.csv"))
    plot_by_treatment(os.path.join(csv_dir, "by_treatment.csv"))



