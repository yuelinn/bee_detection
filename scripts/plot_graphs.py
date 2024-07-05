#!/usr/bin/env python3
"""Script to plot graphs 
with classes, we should be able to plot all the graphs nicely
"""

import os
import glob
from split_dataset import count_instance
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import copy


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

    def ave(self, denum):
        bees_averaged = copy.deepcopy(self)
        bees_averaged.honeybees /= denum
        bees_averaged.bumblebees /= denum
        bees_averaged.unknownbees /= denum
        bees_averaged.total_bees /= denum 
        return bees_averaged


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

    def ave(self, denum):
        bees_averaged = Bees_unflattened()
        bees_averaged.bees_new = self.bees_new.ave(denum)
        bees_averaged.bees_old = self.bees_old.ave(denum)
        bees_averaged.bees_overlaped = self.bees_overlaped.ave(denum)
        bees_averaged.bees_total = self.bees_total.ave(denum)
        return bees_averaged


class OnePlot():
    def __init__(self, fp_list, plot_tag, plot_area=1.0):
        self.parent_fp_list = fp_list
        self.plot_tag = plot_tag

        self.fp_list = []
        self.set_paths()

        self.__bees = Bees_unflattened()
        self.set_bees()

        self.plot_area = plot_area

    def set_paths(self):
        # TODO im sure i can make this prettier but not rn
        for fp in self.parent_fp_list:
            if self.plot_tag in fp:
                self.fp_list.append(fp)

    def set_bees(self):
        for path in self.fp_list:
            count=count_instance(path, 9)
            new_bee = Bees_unflattened(count)
            self.__bees.add(new_bee)

    def get_bees(self):
        if IS_AVE:
            return self.get_average_bees()
        else:
            return self.__bees

    def get_average_bees(self):
        if len(self.fp_list) <= 0:
            ave_bees = self.__bees
        else:
            ave_bees = self.__bees.ave((len(self.fp_list)-1) * self.plot_area * HZ_FACTOR)
        return ave_bees


class OneDay():
    # plot_tags_list = ["PM75", "F", "P", "FM"]
    plot_tags_list = ["PM", "WF", "PH", "WM"]
    # plot_tags_list = ["PM", "PH", "WM", "WF"]
    def __init__(self, day_tag, labels_dir, is_no_plots=False, plots_areas=None):
        self.tag = day_tag
        self.bees = Bees_unflattened()

        self.paths = None
        self.set_paths(labels_dir)
        self.plots_areas = plots_areas

        self.plots = []
        if is_no_plots:
            self.plots.append(OnePlot(self.paths, ""))
        else:
            self.set_plots()

        self.set_total_bees()

    def set_paths(self, labels_dir):
        self.paths = glob.glob(os.path.join(labels_dir, self.tag+"*"))

        # remove blacklist files
        for black_fn in BLACKLIST:
            try:
                self.paths.remove(os.path.join(labels_dir, black_fn))
            except:
                pass


    def set_plots(self):
        for plot_tag, plot_area in zip(OneDay.plot_tags_list, self.plots_areas):
            self.plots.append(OnePlot(self.paths, plot_tag, plot_area))

    def set_total_bees(self):
        for plot in self.plots:
            self.bees.add(plot.get_bees())

    def get_total_bees(self):
        return self.bees


class OneRound():
    day_tags_dict = {}

    day_tags_dict["220710"] = [0.6926,0.7105,0.8616,0.8419]  # PM75  & F  & P  & FM
    day_tags_dict["220717"] = [0.5110,0.9221,0.7286,0.6926]
    day_tags_dict["220719"] = [0.7654,0.6749,0.6403,0.7105]
    day_tags_dict["220720"] = [0.9221,0.9017,0.9427,0.7842]
    day_tags_dict["220721"] = [0.9221,1.1384,0.9635,0.8032]

    """Old camera constant
    day_tags_dict["220710"] = [0.68, 0.70, 0.85, 0.83]  # PM75  & F  & P  & FM
    day_tags_dict["220717"] = [0.50, 0.91, 0.72, 0.68] 
    day_tags_dict["220719"] = [0.75, 0.66, 0.63, 0.70]
    day_tags_dict["220720"] = [0.91, 0.89, 0.93, 0.77]
    day_tags_dict["220721"] = [0.91, 1.12, 0.95, 0.79]
    """

    """
    day_tags_dict["220710"] = [1.0, 1.0, 1.0, 1.0]  # PM75  & F  & P  & FM
    day_tags_dict["220717"] = [1.0, 1.0, 1.0, 1.0]
    day_tags_dict["220719"] = [1.0, 1.0, 1.0, 1.0]
    day_tags_dict["220720"] = [1.0, 1.0, 1.0, 1.0]
    day_tags_dict["220721"] = [1.0, 1.0, 1.0, 1.0]
    """

    day_tags_dict["2021"] = None

    def __init__(self, round_num, labels_dir):
        self.round_num = round_num
        self.labels_dir = labels_dir

        self.days_list = []
        self.populate_days()

    def populate_days(self):
        for day_tag in OneRound.day_tags_dict:
            if day_tag == "2021":
                # handle smartphone as a single plot 
                self.days_list.append(OneDay(day_tag, self.labels_dir, is_no_plots=True))
            else:
                self.days_list.append(OneDay(day_tag, self.labels_dir, plots_areas=OneRound.day_tags_dict[day_tag]))

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

        ax.bar_label(rects, padding=3, fontsize=12, fmt="%.2f")
        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by days')
    ax.set_xticks(x + width, [x.tag for x in round0.days_list], fontsize=font_size)
    ax.legend(loc='upper right')
    if IS_AVE:
        ax.set_ylim(0, AVE_Y_MAX)
    else:
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
        ax.bar_label(rects, padding=3, fontsize=12, fmt="%.2f") 
        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by cultivar')
    ax.set_xticks(x + 2*width, OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right')
    if IS_AVE:
        ax.set_ylim(0, 6)
    else:
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

    ax.bar_label(rects, padding=0, fontsize=font_size, fmt="%.2f")

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees by days')
    ax.set_xticks(x, [x.tag for x in round0.days_list], fontsize=font_size)
    ax.legend(loc='upper right')
    if IS_AVE:
        ax.set_ylim(0, 4000)
    else:
        ax.set_ylim(0, 1000)

    plt.savefig(f"cum_round{round0.round_num}.png")
    plt.close()


# stats per plot, but stacked to show cummulative 
def stats_per_plot_per_class_cum(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(14.,10.))
    x = np.arange(len(OneDay.plot_tags_list))  # FIXME the label locations
    width = 0.5  # the width of the bars
    # multiplier = 0
    font_size = 22
    bottom = np.zeros(len(OneDay.plot_tags_list))
    bees_dict = {}

    for plot in OneDay.plot_tags_list:
        bees_dict[plot] = Bees()

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue

        for plot in day.plots:
            bees_dict[plot.plot_tag].add(plot.get_bees().bees_total)

    offset = 0

    # honey bees
    heights = []
    for plot_tag in bees_dict:
        heights.append(bees_dict[plot_tag].honeybees)
    rects = ax.bar(x + offset, heights, width, label="honeybee", bottom=bottom)
    bottom += heights
    ax.bar_label(rects, padding=0, fontsize=font_size, fmt="%.0f", label_type="center") 

    # bumblebees
    heights = []
    for plot_tag in bees_dict:
        heights.append(bees_dict[plot_tag].bumblebees)
    rects = ax.bar(x + offset, heights, width, label="bumblebee", bottom=bottom)
    bottom += heights
    ax.bar_label(rects, padding=0, fontsize=font_size, fmt="%.0f", label_type="center") 

    # unknown bees 
    heights = []
    for plot_tag in bees_dict:
        heights.append(bees_dict[plot_tag].unknownbees)
    rects = ax.bar(x + offset, heights, width, label="unidentified\ninsect", bottom=bottom)
    bottom += heights

    ax.bar_label(rects, padding=0, fontsize=font_size, fmt="%.0f", label_type="center") 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of individuals ($\mathregular{h^{-1}m^{-2}}$)', fontsize=font_size)
    ax.set_xlabel('Treatment', fontsize=font_size)
    # ax.set_title('Number of individuals ($\mathregular{h^{-1}m^{-2}}$) by treatment and insect taxon', fontsize=font_size)
    ax.set_xticks(x , ["PM75", "F", "P", "FM"], fontsize=font_size)
    # ax.set_xticks(x , OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right', title="Insect taxon")
    if IS_AVE:
        ax.set_ylim(0, 3500)
    else:
        ax.set_ylim(0, 1000)

    plt.savefig(f"cum_plots_by_class_round{round0.round_num}_notitle.png")
    plt.close()



# stats per plot, but stacked to show cummulative 
def stats_per_plot_cum(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(14.,10.))
    x = np.arange(len(OneDay.plot_tags_list))  # FIXME the label locations
    width = 0.5  # the width of the bars
    # multiplier = 0
    font_size = 22
    bottom = np.zeros(len(OneDay.plot_tags_list))
    day_list = [
            "July 10",
            "July 17",
            "July 19",
            "July 20",
            "July 21",
            ]

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        heights = [plot.get_bees().bees_total.total_bees for plot in day.plots]
        # offset = width * multiplier
        offset = 0
        rects = ax.bar(x + offset, heights, width, label=day.tag, bottom=bottom)
        # multiplier += 1
        bottom += heights
    ax.bar_label(rects, padding=0, fontsize=font_size, fmt="%.0f") 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of individuals ($\mathregular{h^{-1}m^{-2}}$)', fontsize=font_size)
    ax.set_xlabel('Treatment', fontsize=font_size)
    # ax.set_title('Number of individuals ($\mathregular{h^{-1}m^{-2}}$) by treatment and date', fontsize=font_size)
    ax.set_xticks(x , ["PM75", "F", "P", "FM"], fontsize=font_size)
    # ax.set_xticks(x , OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right', title="Dates", labels=day_list)
    if IS_AVE:
        ax.set_ylim(0, 3500)
    else:
        ax.set_ylim(0, 1000)

    plt.savefig(f"cum_plots_round{round0.round_num}_notitle.png")
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
            plots_dict[plot.plot_tag].append(plot.get_bees())
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
        ax.bar_label(rects, padding=3, fontsize=12, fmt="%.2f") 
        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees per day by cultivar')
    ax.set_xticks(x + 1.5*width, day_list, fontsize=font_size)
    ax.legend(loc='upper right')
    if IS_AVE:
        ax.set_ylim(0, AVE_Y_MAX)
    else:
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
            plots_dict[plot.plot_tag].append(plot.get_bees())
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
    ax.bar_label(rects, padding=3, fontsize=font_size, fmt="%.2f") 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of bees per day by cultivar')
    ax.set_xticks(x , day_list, fontsize=font_size)
    ax.legend(loc='upper right')
    if IS_AVE:
        ax.set_ylim(0, AVE_Y_MAX)
    else:
        ax.set_ylim(0, 1000)

    plt.savefig(f"cum_day_plots_round{round0.round_num}.png")
    plt.close()


# stats per day per plot, w class breakdown
def print_stats_per_day_by_plots_class(round0):
    plots_dict = {}
    day_list = []

    for plot_tag in OneDay.plot_tags_list:
        plots_dict[plot_tag] = []

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        for plot in day.plots:
            plots_dict[plot.plot_tag].append(plot.get_bees())
        day_list.append(day.tag)

    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(plots_dict[OneDay.plot_tags_list[0]]))  # FIXME the label locations
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    width = 0.2  # the width of the bars
    multiplier = 0
    font_size = 22

    for day_i in range(len(plots_dict[plot_tag])):
        print("day", day_i)
        for plot_tag in plots_dict:
            print("{:.2f}".format(plots_dict[plot_tag][day_i].bees_total.honeybees), end=' & ')
        for plot_tag in plots_dict:
            print("{:.2f}".format(plots_dict[plot_tag][day_i].bees_total.bumblebees), end=' & ')
        for plot_tag in plots_dict:
            print("{:.2f}".format(plots_dict[plot_tag][day_i].bees_total.unknownbees), end=' & ')
        print()



# stats per day per plot, w class breakdown
def stats_per_day_by_plots_class(round0):
    plots_dict = {}
    # day_list = []
    day_list = [
            "July 10",
            "July 17",
            "July 19",
            "July 20",
            "July 21",
            ]

    for plot_tag in OneDay.plot_tags_list:
        plots_dict[plot_tag] = []

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        for plot in day.plots:
            plots_dict[plot.plot_tag].append(plot.get_bees())
        # day_list.append(day.tag)



    fig, ax = plt.subplots(layout='constrained', figsize=(14.,10.))
    x = np.arange(len(plots_dict[OneDay.plot_tags_list[0]]))  # FIXME the label locations
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    width = 0.2  # the width of the bars
    multiplier = 0
    font_size = 22
    plot_tag_paper_list = ["PM75", "F", "P", "FM"]

    for plot_tag, plot_tag_paper in zip(plots_dict, plot_tag_paper_list):
        bottom = np.zeros(len(plots_dict[plot_tag]))
        offset = width * multiplier

        heights = [bees.bees_total.honeybees for bees in plots_dict[plot_tag]]
        rects_h = ax.bar(x + offset, heights, width, label=f"{plot_tag}_honeybee", bottom=bottom, color="tab:blue")
        bottom += heights
        # ax.bar_label(rects, fontsize=12, fmt="%.2f") 

        heights = [bees.bees_total.bumblebees for bees in plots_dict[plot_tag]]
        rects_b = ax.bar(x + offset, heights, width, label=f"{plot_tag}_bumblebee", bottom=bottom, color="tab:green")
        bottom += heights
        # ax.bar_label(rects, fontsize=12, fmt="%.2f") 

        heights = [bees.bees_total.unknownbees for bees in plots_dict[plot_tag]]
        rects_u = ax.bar(x + offset, heights, width, label=f"{plot_tag}_unknown bee", bottom=bottom, color="tab:orange")
        # ax.bar_label(rects, fontsize=12, fmt="%.2f") 

        ax.bar_label(rects_u, padding=20, fontsize=12, fmt="%.0f") 
        bottom += heights
        for xnew, h, in zip(x+offset,bottom):
            plt.text(xnew, h+ 10, plot_tag_paper, ha="center",fontsize=12)

        multiplier += 1

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of individuals ($\mathregular{h^{-1}m^{-2}}$)', fontsize=font_size)
    ax.set_xlabel('Date', fontsize=font_size)
    # ax.set_title('Number of individuals for each day and treatment ($\mathregular{h^{-1}m^{-2}}$)', fontsize=font_size)
    ax.set_xticks(x + 1.5*width, day_list, fontsize=font_size)
    ax.legend(
            loc='upper right', 
            handles=[rects_h, rects_b, rects_u], 
            labels=["honeybee", "bumblebee", "unidentified insect"], 
            title="Insect taxon")
    if IS_AVE:
        ax.set_ylim(0, 1800)
    else:
        ax.set_ylim(0, 600)


    plt.savefig(f"day_plots_cls_round{round0.round_num}_no_title.png")
    plt.close()


# num of images taken
def num_of_pics(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(OneDay.plot_tags_list))  # FIXME the label locations
    width = 0.5  # the width of the bars
    # multiplier = 0
    font_size = 22
    bottom = np.zeros(len(OneDay.plot_tags_list))

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        heights = [len(plot.fp_list) for plot in day.plots]
        # offset = width * multiplier
        offset = 0
        rects = ax.bar(x + offset, heights, width, label=day.tag, bottom=bottom)
        # multiplier += 1
        bottom += heights
        ax.bar_label(rects, padding=0, fontsize=font_size, label_type="center") 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of images', fontsize=font_size)
    ax.set_title('Number of images taken')
    ax.set_xticks(x , OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1000)

    plt.savefig(f"imgs_cum_plots_round{round0.round_num}.png")
    plt.close()


# plot fov
def fov_area(round0):
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    x = np.arange(len(OneDay.plot_tags_list))  # FIXME the label locations
    width = 0.5  # the width of the bars
    # multiplier = 0
    font_size = 22
    bottom = np.zeros(len(OneDay.plot_tags_list))

    for day in round0.days_list:
        if day.tag == "2021":  # TODO make this a tag of the instance instead
            continue
        heights = [plot.plot_area for plot in day.plots]
        # offset = width * multiplier
        offset = 0
        rects = ax.bar(x + offset, heights, width, label=day.tag, bottom=bottom)
        # multiplier += 1
        bottom += heights
    ax.bar_label(rects, padding=0, fontsize=font_size, fmt="%.2f") 

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of bees', fontsize=font_size)
    ax.set_title('Number of images taken')
    ax.set_xticks(x , OneDay.plot_tags_list, fontsize=font_size)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 10)

    plt.savefig(f"fov_area_cum_plots_round{round0.round_num}.png")
    plt.close()


def stats_per_round(rounds_dict):
    """Draw line graph for how stats change across rounds
    """
    fig, ax = plt.subplots(layout='constrained', figsize=(12.,10.))
    font_size = 22

    x = [0, 1, 2, 3, 4, 5]
    total_bees = []
    total_honey = []
    total_bumble = []
    total_unknown = []

    for round_id in x:
        total_bees.append(int(rounds_dict[str(round_id)].get_total_bees().bees_total.total_bees))
        total_honey.append(int(rounds_dict[str(round_id)].get_total_bees().bees_total.honeybees))
        total_bumble.append(int(rounds_dict[str(round_id)].get_total_bees().bees_total.bumblebees))
        total_unknown.append(int(rounds_dict[str(round_id)].get_total_bees().bees_total.unknownbees))

    # total bees 
    ax.plot(x, total_honey, "o-")
    ax.plot(x, total_bumble, "o-")
    ax.plot(x, total_unknown, "o-")
    ax.plot(x, total_bees, "o-")

    plt.rcParams.update({'font.size': font_size})
    ax.tick_params(labelsize=font_size)
    ax.set_ylabel('No. of individuals', fontsize=font_size)
    ax.set_xlabel('Round', fontsize=font_size)
 
    ax.legend(loc='upper right', labels=[
        "honey bees", 
        "bumblebees", 
        "unknown insects",
        "sum of individuals", 
        ])
    ax.set_title('Number of annotated individuals by round')
    ax.set_ylim(0, 3000)
    ax.grid()
    plt.savefig(f"num_bees_by_round_line_graph.png")
    plt.close()

    # print numbers for table
    for i, round_id in enumerate(x):
        print(f"{round_id} & {total_honey[i]} & {total_bumble[i]} & {total_unknown[i]} & {total_bees[i]} \\\\")

if __name__ == "__main__":
    # is_rounds_style= True
    is_rounds_style= False

    IS_AVE = True  # i know this sucks but okay
    # IS_AVE = False
    
    img_dt = 10  # 10s between images 
    HZ_FACTOR = img_dt / 3600 

    AVE_Y_MAX = 4000  # only for ave

    blacklist_fp = "blacklist_labels_fn.txt"  
    blacklist_f = open(blacklist_fp, "r")
    BLACKLIST = [x.strip() for x in blacklist_f.readlines()] # what, another global variable??!!

    if is_rounds_style:
        BLACKLIST = []
        IS_AVE=False


    rounds_dict = {}

    rounds_dict["0"] = OneRound(0, "/media/linn/export10tb/bees/dataset_old/cp_datasets/alles/labels")
    rounds_dict["0.5"] = OneRound(0.5, "/mnt/mon13/bees/runs/detect/round1/labels")
    rounds_dict["1"] = OneRound(1, "/media/linn/export10tb/bees/iterative_labelling/round1_ds/qced/alles_unflattened/labels")
    rounds_dict["1.5"] = OneRound(1.5, "/mnt/mon13/bees/hiwiNr1Nr2_unchecked/labels/labels")
    rounds_dict["2"] = OneRound(2, "/media/linn/export10tb/bees/iterative_labelling/round2_ds/qced/alles_unflattened/labels")
    rounds_dict["2.5"] = OneRound(2.5, "/mnt/mon13/bees/hiwiNr1Nr2r3_unchecked/labels")
    rounds_dict["3"] = OneRound(3, "/media/linn/export10tb/bees/iterative_labelling/round3_ds/qced/alles_unflattened/labels")
    rounds_dict["3.5"] = OneRound(3.5, "/mnt/mon13/bees/hiwiNr1-4_unchecked/labels")
    rounds_dict["4"] = OneRound(4, "/media/linn/export10tb/bees/iterative_labelling/round4_ds/qced/alles_unflattened/labels")
    rounds_dict["4.5"] = OneRound(4.5, "/mnt/mon13/bees/hiwiNr1-5_unchecked/labels")
    rounds_dict["5"] = OneRound(5, "/media/linn/export10tb/bees/iterative_labelling/round5_ds/qced/alles_unflattened/labels")

    if not is_rounds_style:
        for round_key in rounds_dict:
            rounds_dict[round_key].print_round()     # stats per round
            stats_per_day(rounds_dict[round_key])  # stats of days per round
            stats_per_plot(rounds_dict[round_key])  # stats of days per plot
            stats_per_day_cum(rounds_dict[round_key])  # stats of days per round, stacked bar 
            stats_per_plot_cum(rounds_dict[round_key])  # stats of days per plot, stacked bar
            stats_per_day_by_plots(rounds_dict[round_key])
            stats_per_day_by_plots_cum(rounds_dict[round_key])
            stats_per_day_by_plots_class(rounds_dict[round_key])
            stats_per_day_by_plots_class(rounds_dict[round_key])
            num_of_pics(rounds_dict[round_key])
            fov_area(rounds_dict[round_key])
            stats_per_plot_per_class_cum(rounds_dict[round_key])  # stats of days per plot, stacked bar
        print_stats_per_day_by_plots_class(rounds_dict["5"])
    else:
        stats_per_round(rounds_dict)

