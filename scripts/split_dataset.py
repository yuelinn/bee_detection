#!/usr/bin/env python3


from os.path import join 
import numpy as np 
from sklearn.model_selection import train_test_split
import pdb
import shutil
import os


def print_stats(count, tag):
    total = np.sum(count)
    print(f"count_{tag}: {count}, total {tag}: {total}, percentages {tag}: {count/total*100.}")

def count_instance(parent_file, num_classes):
    count=np.zeros(num_classes)
    # open file 
    f = open(parent_file, 'r')
    f_l = f.readlines()
    c_l = [int(obj[0]) for obj in f_l]
    np_c = np.unique(c_l, return_counts=True)

    #  TODO FUCK
    for i, c in enumerate(np_c[0]):
        count[c]=np_c[1][i]

    return count



def count_instance_dir(label_dir, num_classes):
    count=np.zeros(num_classes)

    for fn in os.listdir(label_dir):
        # TODO check valid label file
        count = count + count_instance(join(label_dir, fn), num_classes)

    return count 


def write_l_to_file(fp, l):
    f = open(fp, 'w')
    f.write(''.join(l))

def move_to_dir(target_dir, source_l, parent_dir):
    target_dir_imgs = join(target_dir, "images")
    target_dir_labels = join(target_dir, "labels")
    os.mkdir(target_dir)
    os.mkdir(target_dir_imgs)
    os.mkdir(target_dir_labels)

    for fn in source_l:
        shutil.copy2(join(parent_dir, fn), target_dir_imgs)
        label_fn = fn.split('.')[0] + ".txt" # also move to labels
        shutil.copy2(join(parent_dir, label_fn), target_dir_labels)


if __name__ == "__main__":
    # WARNING: before you use this script, you need to change the train.txt 
    # from CVAT to a txt for each day, and concat all of the days into one large full.txt

    # parent_dir="/home/yl/phd/bees/labels"
    parent_dir="/media/linn/7ABF-E20F/bees/labels"
    test_split = 0.1
    val_split = 0.1

    full_txt=join(parent_dir, "full.txt")
    num_classes = 3

    full_l = open(full_txt, 'r').read().splitlines() 


    # count = count_instance_dir(parent_dir, num_classes)
    # print(f"total count: {count}")

    # split the data 
    train_l, test_l, _, _ = train_test_split(full_l, full_l, 
                                             test_size=test_split, 
                                             random_state=2378)

    train_l, val_l, _, _ = train_test_split(train_l, train_l, 
                                         test_size=int(val_split*len(full_l)), 
                                         random_state=2378)

    print(f"train size: {len(train_l)}\nval size: {len(val_l)}\ntest size: {len(test_l)}")

    # write to file [OPTIONAL]
    # train_txt = join(parent_dir,"train.txt")
    # test_txt = join(parent_dir,"test.txt")
    # val_txt = join(parent_dir,"val.txt")
    # write_l_to_file(train_txt, train_l)
    # write_l_to_file(test_txt, test_l)
    # write_l_to_file(val_txt, val_l)

    # move files to separate dirs based on lists
    train_dir = join(parent_dir, "train")
    test_dir = join(parent_dir, "test")
    val_dir = join(parent_dir, "val")
    move_to_dir(train_dir, train_l, parent_dir)
    move_to_dir(test_dir, test_l, parent_dir)
    move_to_dir(val_dir, val_l, parent_dir)

    # FIXME change dir to follow vars
    count_val=count_instance_dir("/media/linn/7ABF-E20F/bees/labels/val/labels/", 3)
    count_train=count_instance_dir("/media/linn/7ABF-E20F/bees/labels/train/labels/", 3)
    count_test=count_instance_dir("/media/linn/7ABF-E20F/bees/labels/test/labels/", 3)

    print_stats(count_train, "train")
    print_stats(count_val, "val")
    print_stats(count_test, "test")
