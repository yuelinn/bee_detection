#!/usr/bin/env python3
"""A script to merge hiwi labels and all yolo rounds labels
the idea is that each round will have different class numbers

eg:
hiwi labelled honeybee: 0
hiwi labelled bumblebee: 1
hiwi labelled unknown_bee: 2

round1-yolo-pred(+linn corrected) labelled honeybee: 3
round1-yolo-pred(+linn corrected) labelled bumblebee: 4
round1-yolo-pred(+linn corrected) labelled unknown_bee: 5

round1-yolo-pred(high iou) labelled honeybee: 6
round1-yolo-pred(high iou) labelled bumblebee: 7
round1-yolo-pred(high iou) labelled unknown_bee: 8

round2-yolo-pred(+linn corrected) labelled honeybee: 9
round2-yolo-pred(+linn corrected) labelled bumblebee: 10
round2-yolo-pred(+linn corrected) labelled unknown_bee: 11


round2-yolo-pred(high iou) labelled honeybee: 12
round2-yolo-pred(high iou) labelled bumblebee: 13
round2-yolo-pred(high iou) labelled unknown_bee: 14

"""

import click
from tqdm import tqdm 
import os
import pdb
import shutil
import glob


def labels2list(file_f):
    annos_og = file_f.readlines()

    # remove whitespaces
    annos = [anno.translate(str.maketrans('', '', '\n\t\r')) for anno in annos_og]
    annos = [anno.split(' ') for anno in annos]
    return annos 

class id_mapper:
    """Maps class ids from the usual to that of the round
    ids are always strings 
    """
    def __init__(self, round_i, num_classes=3):
        self.round_i = round_i
        self.num_classes = num_classes
        
    def get_new_id(self, old_id):
        return str(self.round_i * self.num_classes + int(old_id))

    def convert_obj_line(self, obj_line_list):
        new_line_list = list(obj_line_list)
        new_line_list[0] = self.get_new_id(obj_line_list[0])
        # remove confidence thing 
        new_line_list.pop()
        return new_line_list


def main(hiwi_labels_dir, round_x_labels_dir, out_dir, overlap_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(overlap_dir, exist_ok=True)

    # copy over files from hiwis labels
    for label_fn in os.listdir(hiwi_labels_dir):
        ori_fp = os.path.join(hiwi_labels_dir, label_fn)
        new_fp = os.path.join(out_dir, label_fn)
        shutil.copy(ori_fp, new_fp)

    # for each round
    for round_i, round_labels_dir in enumerate(round_x_labels_dirs):
        print(f"Starting round {round_i} from dir {round_labels_dir}...")
        round_id_mapper = id_mapper(round_i + 1 )

        for labels_fn in tqdm(os.listdir(round_labels_dir)):
            labels_fp = os.path.join(round_labels_dir, labels_fn)
            combined_labels_fp = os.path.join(out_dir, labels_fn)
            overlap_labels_fp = os.path.join(overlap_dir, labels_fn)

            with open(combined_labels_fp, "a+") as combined_labels_f:
                with open(overlap_labels_fp, "a+") as overlap_labels_f:
                    with open(labels_fp, "r") as round_labels_f:
                        # handling that fucking new line shit 
                        combined_labels_f.seek(0)
                        first_line = combined_labels_f.readline()
                        if first_line:
                            combined_labels_f.write("\n")

                        round_labels_list = labels2list(round_labels_f)
                        for obj_line in round_labels_list:
                            new_obj_line_l = round_id_mapper.convert_obj_line(obj_line)  # change class id of line wrt round
                            new_obj_line_str = " ".join(new_obj_line_l) +"\n"

                            # write to new file 
                            combined_labels_f.write(new_obj_line_str)


if __name__ == '__main__':
    hiwi_labels_dir = "/media/linn/export10tb/bees/dataset_old/cp_datasets/alles/labels"
    round_x_labels_dirs = ["/mnt/mon13/bees/runs/detect/round1/labels"]
    out_dir = "/mnt/mon13/bees/hiwiNr1_unchecked/labels"
    dir_for_overlapped_labels = "/mnt/mon13/bees/hiwiNr1_unchecked/overlapped"
    min_iou_overlap = 0.75

    main(hiwi_labels_dir, round_x_labels_dirs, out_dir, dir_for_overlapped_labels)

