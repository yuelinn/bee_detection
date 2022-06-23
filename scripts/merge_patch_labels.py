#!/usr/bin/env python3
import os
import pdb
import copy
import numpy as np


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
        annos_og = open(os.path.join(merged_fp, filename), 'r').readlines()
        if len(annos_og) == 0:
            continue

        # put annos into a numpy array with 5 cols:
        # [min_x min_y max_x max_y class_id]

        # remove whitespaces
        annos = [anno.translate(str.maketrans('', '', '\n\t\r')) for anno in annos_og]
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

        annos_sorted=annos_corners[annos_corners[:,0].argsort()]
        pivot = annos_sorted[:-1]
        next_box = annos_sorted[1:]

        is_no_overlap_x = next_box[:,0] > pivot[:,2] # minx_new > maxx_pivot

        if np.all(is_no_overlap_x): # no overlap in x-coord
            continue
        else:
            # there may be some overlap based on the x-coordinates
            for i, bb_pivot in enumerate(annos_sorted[:-1]):
                if np.any(np.isnan(bb_pivot)):
                    continue

                is_overlap_x = bb_pivot[2] >= annos_sorted[i+1:,0] # maxx_pivot >= minx_new 
                # (StartA <= EndB) and (EndA >= StartB): miny_pivot <= maxy_new and maxy_pivot >= miny_new
                is_overlap_y = (bb_pivot[1] <= annos_sorted[i+1:,3]) & (bb_pivot[3] >= annos_sorted[i+1:,1])

                if np.any(is_overlap_x & is_overlap_y):
                    remainding_bbs = annos_sorted[i+1:]
                    ol_bbs=remainding_bbs[is_overlap_x & is_overlap_y]

                    # replace pivot bb with larger bounding boxes 

                    if not (np.all(ol_bbs[:,-1] == bb_pivot[-1])):
                        # class should be the same to merge or else alert and skip
                        print(f"In file {filename}: skipping merging {ol_bbs} and {bb_pivot} because the classes do not match")
                        continue
                    else:
                        print(f"In file {filename}: merging {ol_bbs} and {bb_pivot}")


                    # replace current pivot with new bb 
                    new_min_x = min(ol_bbs[:,0].min(), 
                                    ol_bbs[:,2].min(), 
                                    bb_pivot[0])
                    new_max_x = max(ol_bbs[:,0].max(), 
                                    ol_bbs[:,2].max(), 
                                    bb_pivot[2])
                    new_min_y = min(ol_bbs[:,1].min(), 
                                    ol_bbs[:,3].min(), 
                                    bb_pivot[1])
                    new_max_y = max(ol_bbs[:,1].max(), 
                                    ol_bbs[:,3].max(), 
                                    bb_pivot[3])


                    # put the new bb into the pivot 
                    annos_sorted[i,0] = new_min_x
                    annos_sorted[i,1] = new_min_y
                    annos_sorted[i,2] = new_max_x
                    annos_sorted[i,3] = new_max_y

                    # remove overlapping bb since they have been processed
                    annos_sorted[i+1:][is_overlap_x & is_overlap_y,0] = np.NAN
                    annos_sorted[i+1:][is_overlap_x & is_overlap_y,1] = np.NAN
                    annos_sorted[i+1:][is_overlap_x & is_overlap_y,2] = np.NAN
                    annos_sorted[i+1:][is_overlap_x & is_overlap_y,3] = np.NAN
                    annos_sorted[i+1:][is_overlap_x & is_overlap_y,4] = np.NAN




            if np.any(np.isnan(annos_sorted)): # if there is any overlaps

                # remove nan rows
                annos_sorted = annos_sorted[~np.isnan(annos_sorted).any(axis=1)]

                # rescale to the YOLO format 
                annos_yolo = np.zeros(annos_sorted.shape)
                annos_yolo[:,0] = annos_sorted[:,-1]
                annos_yolo[:,1] = (annos_sorted[:,0] +  annos_sorted[:,2])/2.  # c_x
                annos_yolo[:,2] = (annos_sorted[:,1] +  annos_sorted[:,3])/2. # c_y
                annos_yolo[:,3] = annos_sorted[:,2] - annos_sorted[:,0] # w
                annos_yolo[:,4] = annos_sorted[:,3] - annos_sorted[:,1] # h

                annos_yolo[:,1] = annos_yolo[:,1] /og_size_x
                annos_yolo[:,3] = annos_yolo[:,3] /og_size_x

                annos_yolo[:,2] = annos_yolo[:,2] /og_size_y
                annos_yolo[:,4] = annos_yolo[:,4] /og_size_y


                # change to list
                annos_yolo_l = annos_yolo.tolist()

                # TODO change the floating point decimal to match CVAT

                # change class_id to int 
                for anno in annos_yolo_l:
                    anno[0] = int(anno[0])
                
                annos_yolo_l_str = [[str(e) for e in anno] for anno in annos_yolo_l]

                annos_yolo_str = '\n'.join([' '.join(anno) for anno in annos_yolo_l_str])

                # overwrite & save to new file 
                annos_w = open(os.path.join(merged_fp, filename), 'w')
                annos_w.write(annos_yolo_str)



if __name__ == "__main__":
    np.set_printoptions(precision=3)

    # TODO: get sizes from images instead  # FIXME: dont use global vars
    patch_size_x= 2353
    patch_size_y=1777
    og_size_x=4608
    og_size_y=3456

    # label_parent_dir = "/home/yl/phd/bees/labels/220521"
    label_parent_dir = "/media/linn/7ABF-E20F/bees/labels/220526/unzipped"
    output_dir = os.path.join(label_parent_dir, "merged")
    merged_fp=os.path.join(output_dir, "obj_train_data")
    os.mkdir(output_dir) # TODO: throw better error  # FIXME put this back 
    os.mkdir(os.path.join(output_dir, "obj_train_data"))

    create_n_merge(label_parent_dir, merged_fp) # create labels files  # FIXME: put back after finished script
    remove_overlaps(merged_fp) # remove overlaps from label files


    # TODO cp OG image to merged dir
    # TODO cp metadata files to merged dir

