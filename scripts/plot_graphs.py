#!/usr/bin/env python3
"""Script to plot graphs 
with classes, we should be able to plot all the graphs nicely
"""

import os
import glob
from split_dataset import count_instance
from matplotlib import pyplot as plt
import numpy as np


class Bees():
    def __init__(self, hb=0, bb=0, ub=0):
        self.honeybees = hb
        self.bumblebees = bb
        self.unknownbees = ub
        self.total_bees = hb + bb + ub

    def add(self, bee2):
        hb = bee2.honeybees
        bb = bee2.bumblebees
        ub = bee2.unknownbees

        self.honeybees += hb
        self.bumblebees += bb
        self.unknownbees += ub
        self.total_bees += hb + bb + ub


class Bees_unflattened():
    def __init__(self, c=None):
        if not c is None:
            # TODO some checks should happen here
            self.bees_old = Bees(c[0], c[1], c[2])
            self.bees_new = Bees(c[3], c[4], c[5])
            self.bees_overlaped = Bees(c[6], c[7], c[8])
        else:
            self.bees_new = Bees()
            self.bees_old = Bees()
            self.bees_overlaped = Bees()

        self.bees_total = Bees()
        self.bees_total.add(self.bees_new)
        self.bees_total.add(self.bees_old)

    def add(self, bees2):
        self.bees_new.add(bees2.bees_new)
        self.bees_old.add(bees2.bees_old)
        self.bees_overlaped.add(bees2.bees_overlaped)
        self.bees_total.add(bees2.bees_total)


class OnePlot():
    def __init__(self, fp_list, plot_tag):
        self.parent_fp_list = fp_list
        self.plot_tag = plot_tag

        self.fp_list = []
        self.set_paths()

        self.bees = Bees_unflattened()
        self.set_bees()

    def set_paths(self):
        # TODO im sure i can make this prettier but not rn
        for fp in self.parent_fp_list:
            if self.plot_tag in fp:
                self.fp_list.append(fp)

    def set_bees(self):
        for path in self.fp_list:
            count=count_instance(path, 9)
            new_bee = Bees_unflattened(count)
            self.bees.add(new_bee)

    def get_bees(self):
        return self.bees


class OneDay():
    plot_tags_list = ["PM", "PH", "WM", "WF"]
    def __init__(self, day_tag, labels_dir, is_no_plots=False):
        self.tag = day_tag
        self.bees = Bees_unflattened()

        self.paths = None
        self.set_paths(labels_dir)

        self.plots = []
        if is_no_plots:
            self.plots.append(OnePlot(self.paths, ""))
        else:
            self.set_plots()

        self.set_total_bees()

    def set_paths(self, labels_dir):
        self.paths = glob.glob(os.path.join(labels_dir, self.tag+"*"))

    def set_plots(self):
        for plot_tag in OneDay.plot_tags_list:
            self.plots.append(OnePlot(self.paths, plot_tag))

    def set_total_bees(self):
        for plot in self.plots:
            self.bees.add(plot.get_bees())

    def get_total_bees(self):
        return self.bees


class OneRound():
    day_tags_list = [
            "220710",
            "220717",
            "220719",
            "220720",
            "220721",
            "2021"
            ]

    def __init__(self, round_num, labels_dir):
        self.round_num = round_num
        self.labels_dir = labels_dir

        self.days_list = []
        self.populate_days()

    def populate_days(self):
        for day_tag in OneRound.day_tags_list:
            if day_tag == "2021":
                # handle smartphone as a single plot 
                self.days_list.append(OneDay(day_tag, self.labels_dir, is_no_plots=True))
            else:
                self.days_list.append(OneDay(day_tag, self.labels_dir))

    def get_total_bees(self):
        bees = Bees_unflattened()
        for day in self.days_list:
            bees.add(day.get_total_bees())
        return bees

    def print_round(self):
        bees = self.get_total_bees().bees_total
        print(f"round{self.round_num}: \thoney: {bees.honeybees},\tbumble: {bees.bumblebees}\tunknown: {bees.unknownbees}\ttotal: {bees.total_bees}")


def stats_per_day(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(round0.days_list))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    font_size = 22

    honey_bees_arr = np.zeros((len(round0.days_list),))  # 5 days and one smartphone
    bumble_bees_arr = np.zeros((len(round0.days_list),))  # 5 days and one smartphone
    unknown_bees_arr = np.zeros((len(round0.days_list),))  # 5 days and one smartphone

    for i_day, day in enumerate(round0.days_list):
        bees = day.get_total_bees().bees_total
        honey_bees_arr[i_day] = bees.honeybees
        bumble_bees_arr[i_day] = bees.bumblebees
        unknown_bees_arr[i_day] = bees.unknownbees
    
    for heights, names in zip(
            [honey_bees_arr, bumble_bees_arr, unknown_bees_arr],
            ["honeybee", "bumblebee", "unknown bee"]
            ):  # i know this is weird

        offset = width * multiplier
        rects = ax.bar(x + offset, heights, width, label=names)

        ax.bar_label(rects, padding=3, fontsize=font_size)
        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by days')
    ax.set_xticks(x + width, [x.tag for x in round0.days_list], fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1000)

    plt.savefig(f"round{round0.round_num}.png")
    plt.close()


# stats per plot
def stats_per_plot(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(OneDay.plot_tags_list))  # FIXME the label locations
    width = 0.15  # the width of the bars
    multiplier = 0
    font_size = 22

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        heights = [plot.get_bees().bees_total.total_bees for plot in day.plots]
        offset = width * multiplier
        rects = ax.bar(x + offset, heights, width, label=day.tag)
        ax.bar_label(rects, padding=3, fontsize=font_size) 
        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by cultivar')
    ax.set_xticks(x + 2*width, OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 600)

    plt.savefig(f"plots_round{round0.round_num}.png")
    plt.close()


# TODO modularise
def stats_per_day_cum(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(round0.days_list))  # the label locations
    bottom = np.zeros(len(round0.days_list))
    width = 0.5  # the width of the bars
    # multiplier = 0
    font_size = 22

    honey_bees_arr = np.zeros((len(round0.days_list),))  # 5 days and one smartphone
    bumble_bees_arr = np.zeros((len(round0.days_list),))  # 5 days and one smartphone
    unknown_bees_arr = np.zeros((len(round0.days_list),))  # 5 days and one smartphone

    for i_day, day in enumerate(round0.days_list):
        bees = day.get_total_bees().bees_total
        honey_bees_arr[i_day] = bees.honeybees
        bumble_bees_arr[i_day] = bees.bumblebees
        unknown_bees_arr[i_day] = bees.unknownbees
    
    for heights, names in zip(
            [honey_bees_arr, bumble_bees_arr, unknown_bees_arr],
            ["honeybee", "bumblebee", "unknown bee"]
            ):  # i know this is weird

        # offset = width * multiplier
        offset = 0
        rects = ax.bar(x + offset, heights, width, label=names, bottom=bottom)
        
        # ax.bar_label(rects, padding=0, fontsize=font_size)
        bottom += heights
        # multiplier += 1

    ax.bar_label(rects, padding=0, fontsize=font_size)

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by days')
    ax.set_xticks(x, [x.tag for x in round0.days_list], fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1000)

    plt.savefig(f"cum_round{round0.round_num}.png")
    plt.close()


# stats per plot, but stacked to show cummulative 
def stats_per_plot_cum(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(OneDay.plot_tags_list))  # FIXME the label locations
    width = 0.5  # the width of the bars
    # multiplier = 0
    font_size = 22
    bottom = np.zeros(len(OneDay.plot_tags_list))

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        heights = [plot.get_bees().bees_total.total_bees for plot in day.plots]
        # offset = width * multiplier
        offset = 0
        rects = ax.bar(x + offset, heights, width, label=day.tag, bottom=bottom)
        # multiplier += 1
        bottom += heights
    ax.bar_label(rects, padding=0, fontsize=font_size) 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by cultivar')
    ax.set_xticks(x , OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1000)

    plt.savefig(f"cum_plots_round{round0.round_num}.png")
    plt.close()


# stats per day per plot
def stats_per_day_by_plots(round0):
    plots_dict = {}
    day_list = []

    for plot_tag in OneDay.plot_tags_list:
        plots_dict[plot_tag] = []

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        for plot in day.plots:
            plots_dict[plot.plot_tag].append(plot.bees)
        day_list.append(day.tag)

    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(plots_dict[OneDay.plot_tags_list[0]]))  # FIXME the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    font_size = 22

    for plot_tag in plots_dict:
        heights = [bees.bees_total.total_bees for bees in plots_dict[plot_tag]]
        offset = width * multiplier
        rects = ax.bar(x + offset, heights, width, label=plot_tag)
        ax.bar_label(rects, padding=3, fontsize=font_size) 
        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees per day by cultivar')
    ax.set_xticks(x + 1.5*width, day_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1000)

    plt.savefig(f"day_plots_round{round0.round_num}.png")
    plt.close()


# stats per day per plot
def stats_per_day_by_plots_cum(round0):
    plots_dict = {}
    day_list = []

    for plot_tag in OneDay.plot_tags_list:
        plots_dict[plot_tag] = []

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        for plot in day.plots:
            plots_dict[plot.plot_tag].append(plot.bees)
        day_list.append(day.tag)

    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(plots_dict[OneDay.plot_tags_list[0]]))  # FIXME the label locations
    bottom = np.zeros(len(day_list))
    width = 0.5  # the width of the bars
    multiplier = 0
    font_size = 22

    for plot_tag in plots_dict:
        heights = [bees.bees_total.total_bees for bees in plots_dict[plot_tag]]
        # offset = width * multiplier
        offset = 0
        rects = ax.bar(x + offset, heights, width, label=plot_tag, bottom=bottom)
        # multiplier += 1
        bottom += heights
    ax.bar_label(rects, padding=3, fontsize=font_size) 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees per day by cultivar')
    ax.set_xticks(x , day_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1000)

    plt.savefig(f"cum_day_plots_round{round0.round_num}.png")
    plt.close()


# stats per day per plot, w class breakdown
def stats_per_day_by_plots_class(round0):
    plots_dict = {}
    day_list = []

    for plot_tag in OneDay.plot_tags_list:
        plots_dict[plot_tag] = []

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        for plot in day.plots:
            plots_dict[plot.plot_tag].append(plot.bees)
        day_list.append(day.tag)

    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(plots_dict[OneDay.plot_tags_list[0]]))  # FIXME the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    font_size = 22

    for plot_tag in plots_dict:
        bottom = np.zeros(len(plots_dict[plot_tag]))
        offset = width * multiplier

        heights = [bees.bees_total.honeybees for bees in plots_dict[plot_tag]]
        rects = ax.bar(x + offset, heights, width, label=f"{plot_tag}_honeybee", bottom=bottom, color="tab:blue")
        bottom += heights

        heights = [bees.bees_total.bumblebees for bees in plots_dict[plot_tag]]
        rects = ax.bar(x + offset, heights, width, label=f"{plot_tag}_bumblebee", bottom=bottom, color="tab:green")
        bottom += heights

        heights = [bees.bees_total.unknownbees for bees in plots_dict[plot_tag]]
        rects = ax.bar(x + offset, heights, width, label=f"{plot_tag}_unknown bee", bottom=bottom, color="tab:orange")

        ax.bar_label(rects, padding=20, fontsize=font_size) 
        bottom += heights
        for xnew, h, in zip(x+offset,bottom):
            plt.text(xnew, h, plot_tag, ha="center",fontsize=18)

        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees per day by cultivar')
    ax.set_xticks(x + 1.5*width, day_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 600)

    plt.savefig(f"day_plots_cls_round{round0.round_num}.png")
    plt.close()


if __name__ == "__main__":

    rounds_dict = {}

    rounds_dict["0"] = OneRound(0, "/media/linn/export10tb/bees/dataset_old/cp_datasets/alles/labels")
    rounds_dict["0.5"] = OneRound(0.5, "/mnt/mon13/bees/runs/detect/round1/labels")
    rounds_dict["1"] = OneRound(1, "/media/linn/export10tb/bees/iterative_labelling/round1_ds/qced/alles_unflattened/labels")
    rounds_dict["1.5"] = OneRound(1.5, "/mnt/mon13/bees/hiwiNr1Nr2_unchecked/labels/labels")
    rounds_dict["2"] = OneRound(2, "/media/linn/export10tb/bees/iterative_labelling/round2_ds/qced/alles_unflattened/labels")
    rounds_dict["2.5"] = OneRound(2.5, "/mnt/mon13/bees/hiwiNr1Nr2r3_unchecked/labels")
    rounds_dict["3"] = OneRound(3, "/media/linn/export10tb/bees/iterative_labelling/round3_ds/qced/alles_unflattened/labels")
    rounds_dict["3.5"] = OneRound(3.5, "/mnt/mon13/bees/hiwiNr1-4_unchecked/labels")

    for round_key in rounds_dict:
        rounds_dict[round_key].print_round()     # stats per round
        stats_per_day(rounds_dict[round_key])  # stats of days per round
        stats_per_plot(rounds_dict[round_key])  # stats of days per plot
        stats_per_day_cum(rounds_dict[round_key])  # stats of days per round, stacked bar 
        stats_per_plot_cum(rounds_dict[round_key])  # stats of days per plot, stacked bar
        stats_per_day_by_plots(rounds_dict[round_key])
        stats_per_day_by_plots_cum(rounds_dict[round_key])
        stats_per_day_by_plots_class(rounds_dict[round_key])





