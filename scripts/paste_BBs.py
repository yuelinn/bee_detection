#!/usr/bin/env python3
"""given a dir of bee snippets, and another dir of full images, paste snippets randomly into full images + create labels
"""

import os
import random
from PIL import Image 
from scipy.stats import multivariate_normal
from tqdm import tqdm


import numpy as np

if __name__ == '__main__':
    # tag = "2022_action_cam_day1"
    parent_dir = "/mnt/bee_cube/dataset_final/2021_2022_all_dataset"
    bee_snippet_dir = f"/mnt/bee_cube/dataset_final/actioncam_5days/train/bee_snippets"
    full_imgs_dir = f"{parent_dir}/train/images"
    output_img_dir = f"{parent_dir}/train/imgs_auged"
    output_labels_dir = f"{parent_dir}/train/labels_auged"

    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)
    
    max_num_bees_per_img = 20
    min_num_bees_per_img = 1
    
    # get list of bee snippets
    bee_snippet_fns = os.listdir(bee_snippet_dir)

    for img_fn in tqdm(os.listdir(full_imgs_dir)):
        # choose random num of bees to put inside
        num_bees = random.randint(min_num_bees_per_img, max_num_bees_per_img)

        # create new label txt 
        label_fn = img_fn.split(".")[0]+ ".txt"
        label_fp = os.path.join(output_labels_dir, label_fn)
        label_f = open(label_fp, "a")

        full_img_pil = Image.open(os.path.join(full_imgs_dir, img_fn))
        full_img_np = np.array(full_img_pil)
        w, h = full_img_pil.size

        # print(num_bees)
        for bee in range(num_bees):
            # randomly choose a bee snippet 
            bee_fn = random.choice(bee_snippet_fns)
            bee_pil = Image.open(os.path.join(bee_snippet_dir,  bee_fn))
            bee_w, bee_h= bee_pil.size
            # perform augmentations for rotations
            rot = random.uniform(0.0,360.0)
            bee_pil = bee_pil.rotate(rot, expand=True, resample=Image.Resampling.BICUBIC)
            # TODO increase augmentation methods, eg. filp, scale etc.

            bee_np = np.array(bee_pil)

            # create the mask 
            x, y = np.mgrid[-1:1:complex(0,bee_h), -1:1:complex(0,bee_w)] # FIXME take care of the odd number case
            pos = np.dstack((x, y))
            rv = multivariate_normal([0.0,0.0], [[0.3, 0.], [0.0, 0.3]])
            gauss = rv.pdf(pos)
            gauss_rotated = np.array(Image.fromarray(gauss).rotate(rot, expand=True, resample=Image.Resampling.BICUBIC)) # FIXME function-ize
            gauss_rotated = gauss_rotated *2. # TODO tuned by hand. maybe add it back to the cov mat
            gauss_rotated[gauss_rotated > 1.] = 1.0
            gauss_rotated = np.expand_dims(gauss_rotated, axis=-1)


            # randomly choose location of bee 
            cx = random.uniform(0.15, 0.85) # FIXME makes sure its within bounds
            cy = random.uniform(0.15, 0.85) # FIXME ditto

            cx_full = int(cx * w)
            cy_full = int(cy * h)
            
            bee_h_rot, bee_w_rot, _ = bee_np.shape
            bee_minx =int(cx_full - bee_w_rot/2)
            bee_miny =int( cy_full - bee_h_rot/2)
            bee_maxx =int( cx_full + bee_w_rot/2)
            bee_maxy =int( cy_full + bee_h_rot/2)

            # paste bee into img (update img)
            try:
                blah = full_img_np[bee_miny:bee_maxy, bee_minx:bee_maxx]
                blah = blah * (1- gauss_rotated) + bee_np* gauss_rotated
                full_img_np[bee_miny:bee_maxy, bee_minx:bee_maxx] = blah
                # TODO make gaussian blur boundaries. hint: use Image.composite, Image.apply_transparency
            except:
                import pdb; pdb.set_trace()
                # FIXME make sure its still within bounds

            # get bee class
            bee_cls  = bee_fn.split("_")[0]
            
            # update label
            label_str = f"{bee_cls} {cx} {cy} {bee_w_rot/w} {bee_h_rot/h}\n"
            label_f.write(label_str)

        img = Image.fromarray(full_img_np)
        img.save(os.path.join(output_img_dir, img_fn))
        label_f.close()


