#!/usr/bin/env python3
"""Script to plot graphs 
with classes, we should be able to plot all the graphs nicely
"""


import os
import glob
from split_dataset import count_instance


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


if __name__ == "__main__":
    round0 = OneRound(0, "/media/linn/export10tb/bees/dataset_old/cp_datasets/alles/labels")

    import pdb; pdb.set_trace()

