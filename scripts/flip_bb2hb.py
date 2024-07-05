#!/usr/bin/env python3
"""A script to flip the labels 
One of the hiwi's labelling tool had the class of honeybee and bumblebee flipped.
So here is a script to fix the f**k-up.
Originally Julian's code.
"""


import numpy as np
import os
import shutil
from PIL import Image
import glob


def flip_labels(path_to_labels, path_to_destination):
    for label_fn in os.listdir(path_to_labels):
        origin = os.path.join(path_to_labels , str(label_fn))
        target = os.path.join(path_to_destination , str(label_fn))
    
        text = open(origin, 'r')
        save_test = open(target, 'w')
        lines = text.readlines()
        # print("LINES:", lines)
        with open(target, 'w') as f:
            for object in lines:
                # print("OBJECT:", object)
                l = object.split(' ')
                # print("Separated lines in List", l)
                if l[0] == "0":
                    l[0] = "1"
                elif l[0] == "1":
                    l[0] = "0"
                #elif l[0] == "2":
                #    l[0] = "2"
                f.write(l[0]+" " + l[1] + " " +l[2] + " " + l[3] + " " +  l[4])
                print("Separated lines in List", l)
        f.close()


if __name__ == '__main__':
    parent_dirs = "/media/linn/export10tb/bees/dataset_old/cp_datasets/2021_smartphone/"
    # parent_dirs = "/media/linn/export10tb/bees/exp_2022/220710/*"

    for plot_dir in glob.glob(parent_dirs):
        path_to_destination = os.path.join(plot_dir, "labels_flipped")
        os.makedirs(path_to_destination)
        path_to_labels = os.path.join(plot_dir, "labels")
        flip_labels(path_to_labels, path_to_destination)
