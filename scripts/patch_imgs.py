#!/usr/bin/env python3

import os
from skimage import io
import pdb 


def patch(img_dir, out_dir, patch_size_x, patch_size_y, overlap):

    imgs=os.listdir(img_dir)
    # print(imgs)
    for img_name in imgs:
        imgpath = os.path.join(img_dir, img_name)
        # dirpath = os.path.join(out_dir, img_name.split('.')[0])
        # os.mkdir(dirpath)

        supported_img_formats = [".JPG", ".jpg", ".png"]

        if any(img_format in imgpath for img_format in supported_img_formats):  
            img_np = io.imread(imgpath)
            ori_width = img_np.shape[1]
            ori_height = img_np.shape[0]
            # print(img_np.shape)

            count = 0 

            top_col_x = 0

            while top_col_x + patch_size_x < ori_width:
                top_row_y = 0 

                while top_row_y + patch_size_y < ori_height:
                    print(top_col_x, top_row_y)
                    patch_name="_"+str(count)+"_"+str(top_row_y)+"_"+str(top_col_x)

                    os.makedirs(os.path.join(out_dir, patch_name), exist_ok=True)

                    # patch_name=img_name.split('.')[0]+"_"+str(count)+"_"+str(top_row_y)+"_"+str(top_col_x)+".jpg"
                    io.imsave(os.path.join(out_dir, patch_name, img_name), 
                              img_np[top_row_y:top_row_y+patch_size_y, top_col_x:top_col_x+patch_size_x])
                    top_row_y = top_row_y + patch_size_y - overlap
                    count+=1
                top_col_x = top_col_x + patch_size_x - overlap
        else:
            print("skipping file", imgpath)



if __name__ == "__main__":
    img_dir = "/home/yl/phd/bees/101_2105"
    out_dir = "/home/yl/phd/bees/101_2105/patches"
    overlap = 100
    patch_size_x = int(4608/2 + overlap/2 -1)
    patch_size_y = int(3456/2 + overlap/2 -1)

    patch(img_dir, out_dir, patch_size_x, patch_size_y, overlap)

