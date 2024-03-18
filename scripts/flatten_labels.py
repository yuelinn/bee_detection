#!/usr/bin/env python3
"""A script to convert the labels encoded of rounds to prepare for training
this is the opposite of the function id_mapper

def get_new_id(self, old_id, is_corr_pred=False):
    if is_corr_pred:  # 6, 7, 8
        new_id = (2 * self.round_i) * (self.num_classes) + int(old_id)
    else:  # 3, 4, 5
        new_id = (2 * self.round_i - 1) * (self.num_classes) + int(old_id)
    return new_id

"""

import os


def get_cls_id(old_id):
    cls_id = old_id % 3
    return cls_id

def convert_line(old_line):
    line_list = old_line.split(' ')
    line_list[0] = str(get_cls_id(int(line_list[0])))
    return ' '.join(line_list)


def class_valid(old_line):
    """some classes should be ignored because they are like, duplicate of hiwi's original label
    classes that should be skipped: 6,7,8 ; 12,13,14; 18,19,20 etc.
    """
    cls = int(old_line.split(' ')[0])
    return not is_skip(cls)

def is_skip(cls):
    return (cls // 6 >= 1) and (cls % 6 < 3)

def test_cls():
    for cls in range(30):
        print(cls, is_skip(cls))

def convert_labels(qced_labels_dir, output_training_dir):
    for label_fn in os.listdir(qced_labels_dir):
        label_fp = os.path.join(qced_labels_dir, label_fn)
        new_label_fp = os.path.join(output_training_dir, label_fn)

        with open(label_fp, "r") as label_f:
            with open(new_label_fp, "w") as new_label_f:
                old_lines = label_f.readlines()
                for old_line in old_lines:
                    if class_valid(old_line):
                        new_line = convert_line(old_line)
                        new_label_f.write(new_line)

def main():
    qced_labels_dir = "/media/linn/export10tb/bees/iterative_labelling/round1_ds/qced/round1-qced-day5/labels"
    output_training_dir = "/media/linn/export10tb/bees/iterative_labelling/round1_ds/qced/round1-qced-day5/labels4training"

    os.makedirs(output_training_dir, exist_ok=True)

    convert_labels(qced_labels_dir, output_training_dir)

if __name__ == '__main__':
    main()
    # test_cls()


