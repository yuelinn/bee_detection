#!/usr/bin/env python3
import os
import pdb
import copy


if __name__ == "__main__":
    label_parent_dir = "/home/yl/phd/bees/labels/220521"
    output_dir = os.path.join(label_parent_dir, "merged")
    merged_fp=os.path.join(output_dir, "obj_train_data")

    # TODO: get sizes from images instead
    patch_size_x= 2353
    patch_size_y=1777
    OG_size_x=4608
    OG_size_y=3456



    # os.mkdir(output_dir) # TODO: throw better error # FIXME put this back 
    # os.mkdir(os.path.join(output_dir, "obj_train_data"))

    # list of patch dirs 
    patches_dir = os.listdir(label_parent_dir)

    classes_list=[]
    
    for patch_dir in patches_dir:
        patch_dir_fp =os.path.join(label_parent_dir, patch_dir)
        if "annotated" in patch_dir and os.path.isdir(patch_dir_fp):
            print("reading from", patch_dir)
            meta_fp=os.path.join(label_parent_dir, patch_dir, "obj.data")

            # compare classes to make sure they are all same 
            classes_fn = "obj.names" 
            classes_fp = os.path.join(patch_dir_fp, classes_fn)
            classes_file = open(classes_fp, 'r')  # TODO: close open files 
            if len(classes_list) == 0:
                classes_list = classes_file.readlines()
                print("found classes :", classes_list)
            else:
                classes_list_new = classes_file.readlines()
                if classes_list != classes_list_new:
                    raise ValueError("classes files do not match!")

            # get offset 
            row_offset = float(patch_dir.split('_')[2])
            col_offset = float(patch_dir.split('_')[3])



            # create new annotations txt to put in merged dir
            data_fp = os.path.join(patch_dir_fp, "obj_train_data")
            for filename in os.listdir(data_fp):

                if ".txt" in filename:
                    anno_out_fp=os.path.join(merged_fp, filename)
                    if not os.path.exists(anno_out_fp):
                        print("creating file", anno_out_fp)
                        out_anno = open(anno_out_fp, "w")
                    else:
                        out_anno = open(anno_out_fp, "a")

                    annos = open(os.path.join(data_fp, filename), 'r').readlines()
                    for anno in annos:
                        anno_list = anno.split()
                        class_id = anno[0]
                        bb_x = (float(anno_list[1]) * patch_size_x + col_offset) / OG_size_x
                        bb_y = (float(anno_list[2]) * patch_size_y + row_offset) / OG_size_y
                        bb_w = float(anno_list[3]) * patch_size_x / OG_size_x
                        bb_h = float(anno_list[4]) * patch_size_y / OG_size_y
                        out_anno.write(' '.join([class_id, 
                                                 "{:.6f}".format(bb_x), 
                                                 "{:.6f}".format(bb_y), 
                                                 "{:.6f}".format(bb_w), 
                                                 "{:.6f}".format(bb_h)]))
                        out_anno.write('\n')


    # FIXME: handle overlapping cases
    for filename in os.listdir(merged_fp):
        print(filename)
        annos = open(os.path.join(merged_fp, filename), 'r').readlines()
        objs = copy.deepcopy(annos)
        out_list = []

        while len(objs) >0:
            pivot = objs[0]
            for obj in objs[1:]:
                # check if overlaps
                if is_overlap:
                    obj_j



        # read all boxes
        # check if boxes overlap:
        # if is_boxes_overlap(boxes_list):
            # just take the biggest box 








            # cp OG image to merged dir
            # cp metadata files to merged dir
