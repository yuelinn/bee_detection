#!/usr/bin/env python3
"""When the labeller does not create an empty label file, this script will.
Originally from Julian
"""


import os


def create_empty_labels(path_to_input_labels, path_to_input_images):
    for n in os.listdir(path_to_input_images):
        according_label = n[:-3] + "txt"
        print(path_to_input_labels + "/" + according_label)
        if not os.path.exists(path_to_input_labels + "/" + according_label):
            with open(path_to_input_labels + "/" + according_label, 'w') as f:
                f.close()


if __name__ == '__main__':

    """
    # for the multiple days action cam
    parent_dir = "/media/linn/export10tb/bees/datasets/2022_action_cam/"

    for date_dir in os.listdir(parent_dir):
        date_path = os.path.join(parent_dir, date_dir)
        imgs_dir = os.path.join(date_path, "images")
        labels_dir = os.path.join(date_path, "labels")
        create_empty_labels(labels_dir, imgs_dir)
    """
    
    # for sabine's smartphone
    parent_dir = "/media/linn/export10tb/bees/datasets/2021_smartphone"
    imgs_dir = os.path.join(parent_dir, "images")
    labels_dir = os.path.join(parent_dir, "labels")
    create_empty_labels(labels_dir, imgs_dir)
 
