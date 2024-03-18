#!/usr/bin/env python3

import os
import glob
from split_dataset import count_instance_dir, print_stats

if __name__ == "__main__":
    split_dirs = "/media/linn/export10tb/bees/dataset_old/cp_datasets/2022_action_cam/*"
    for split_dir in glob.glob(split_dirs):
        print(split_dir)
        count=count_instance_dir(os.path.join(split_dir,"labels"), 3)
        print_stats(count, "train")


