#!/usr/bin/env python3
import os
import pdb
import copy
import numpy as np
import pprint





def create_n_merge(label_parent_dir, merged_fp):



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

            print(f"Setting row offset {row_offset} and col offset {col_offset} for dir {patch_dir}")

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
                        bb_x = (float(anno_list[1]) * patch_size_x + col_offset) / og_size_x
                        bb_y = (float(anno_list[2]) * patch_size_y + row_offset) / og_size_y
                        bb_w = float(anno_list[3]) * patch_size_x / og_size_x
                        bb_h = float(anno_list[4]) * patch_size_y / og_size_y
                        out_anno.write(' '.join([class_id, 
                                                 "{:.6f}".format(bb_x), 
                                                 "{:.6f}".format(bb_y), 
                                                 "{:.6f}".format(bb_w), 
                                                 "{:.6f}".format(bb_h)]))
                        out_anno.write('\n')




def remove_overlaps(merged_fp):
    for filename in os.listdir(merged_fp):
        print(filename)
        annos = open(os.path.join(merged_fp, filename), 'r').readlines()

        # put annos into a numpy array with 5 cols:
        # [min_x min_y max_x max_y class_id]

        # remove whitespaces
        annos = [anno.translate(str.maketrans('', '', '\n\t\r')) for anno in annos]
        annos = [anno.split(' ' ) for anno in annos]
        annos_np = np.array(annos, dtype=np.float64)

        # TODO I really should write a function to do this transformation
        scale_np = np.array([1., og_size_x, og_size_y, og_size_x, og_size_y])
        annos_scaled = annos_np * scale_np
        annos_corners = np.zeros(annos_scaled.shape)
        annos_corners[:,0]=annos_scaled[:,1] - (annos_scaled[:,3]/2) # minx = c_x - w/2
        annos_corners[:,1]=annos_scaled[:,2] - (annos_scaled[:,4]/2) # miny = c_y - h/2
 
        annos_corners[:,2]=annos_scaled[:,1] + (annos_scaled[:,3]/2) # maxx = c_x + w/2
        annos_corners[:,3]=annos_scaled[:,2] + (annos_scaled[:,4]/2) # maxy = c_y + h/2
        annos_corners[:,4]=annos_scaled[:,0]

        annos_sorted=np.sort(annos_corners, axis=0)
        pivot = annos_sorted[:-1]
        next_box = annos_sorted[1:]

        is_no_overlap = next_box[:,0] > pivot[:,2] # minx_new > maxx_pivot

        if not np.all(possible_overlap):
            # there may be some overlap based on the x-coordinates
            pdb.set_trace()





        






            # cp OG image to merged dir
            # cp metadata files to merged dir


if __name__ == "__main__":
    np.set_printoptions(precision=3)

    # TODO: get sizes from images instead  # FIXME: dont use global vars
    patch_size_x= 2353
    patch_size_y=1777
    og_size_x=4608
    og_size_y=3456

    label_parent_dir = "/media/linn/7ABF-E20F/bees/labels/220521/labels"
    output_dir = os.path.join(label_parent_dir, "merged")
    merged_fp=os.path.join(output_dir, "obj_train_data")
    # os.mkdir(output_dir) # TODO: throw better error  # FIXME put this back 
    # os.mkdir(os.path.join(output_dir, "obj_train_data"))

    # create_n_merge(label_parent_dir, merged_fp) # create labels files  # FIXME: put back after finished script
    remove_overlaps(merged_fp) # remove overlaps from label files

