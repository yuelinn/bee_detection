#!/usr/bin/env python3
"""given a dir of bee snippets, and another dir of full images, paste snippets randomly into full images + create labels
"""

import os
import random
from PIL import Image 

import numpy as np

if __name__ == '__main__':
    bee_snippet_dir = "/media/linn/export10tb/bees/dataset_final/datasets_by_days/2022_action_cam_day1/train/bee_snippets"
    full_imgs_dir = "/media/linn/export10tb/bees/dataset_final/datasets_by_days/2022_action_cam_day1/train/images"
    output_img_dir = "/media/linn/export10tb/bees/dataset_final/datasets_by_days/2022_action_cam_day1/train/imgs_auged"
    output_labels_dir = "/media/linn/export10tb/bees/dataset_final/datasets_by_days/2022_action_cam_day1/train/labels_auged"
    max_num_bees_per_img = 100
    min_num_bees_per_img = 1
    
    # get list of bee snippets
    bee_snippet_fns = os.listdir(bee_snippet_dir)

    for img_fn in os.listdir(full_imgs_dir):
        # choose random num of bees to put inside
        num_bees = random.randint(min_num_bees_per_img, max_num_bees_per_img)

        # create new label txt 
        label_fn = img_fn.split(".")[0]+ ".txt"
        label_fp = os.path.join(output_labels_dir, label_fn)
        label_f = open(label_fp, "w")

        full_img_pil = Image.open(os.path.join(full_imgs_dir, img_fn))
        full_img_np = np.array(full_img_pil)
        w, h = full_img_pil.size

        for bee in range(num_bees):
            # randomly choose a bee snippet 
            bee_fn = random.choice(bee_snippet_fns)
            bee_pil = Image.open(os.path.join(bee_snippet_dir,  bee_fn))
            bee_np = np.array(bee_pil)

            # randomly choose location of bee 
            cx = random.uniform(0.015, 0.85)
            cy = random.uniform(0.015, 0.85)
            # FIXME make sure its still within bounds

            cx_full = int(cx * w)
            cy_full = int(cy * h)

            bee_w, bee_h= bee_pil.size

            bee_minx =int(cx_full - bee_w/2)
            bee_miny =int( cy_full - bee_h/2)

            bee_maxx =int( cx_full + bee_w/2)
            bee_maxy =int( cy_full + bee_h/2)

            # paste bee into img (update img)
            try:
                full_img_np[bee_miny:bee_maxy, bee_minx:bee_maxx]=bee_np
            except:
                import pdb; pdb.set_trace()

            # get bee class
            bee_cls  = bee_fn.split("_")[0]
            
            # update label
            label_str = f"{bee_cls} {cx} {cy} {bee_w/w} {bee_h/h}"
            label_f.write(label_str)

        img = Image.fromarray(full_img_np)
        img.save(os.path.join(output_img_dir, img_fn))
        label_f.close()


