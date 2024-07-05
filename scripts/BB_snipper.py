import os
from PIL import Image, ImageOps, ImageDraw
import numpy as np
from tqdm import tqdm

def BB_snipper(label_root_path, export_dest_path, vis_bb_path=None):
    """
    Function to generate the snipped bee images
    label_root_path is the path to the directory, that contains the directories with the images and the labels
    export_dest_path is the path to a directory that is used to save the snipped images

    The outputted image file names are concatenated from:
    The type (honeybee/bumblebee) with their according label number (0/1)
    The center width coordinate in percentage
    The center height coordinate in percentage
    The numbered label inside the image (First label per images receives 1, second receives 2...=
    The filename of the original image
    """

    os.makedirs(export_dest_path, exist_ok=True)

    path_to_input_images = label_root_path+"/images/"
    path_to_label = label_root_path+"/labels/"
    filenames = os.listdir(path_to_input_images)
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')


    for filename in tqdm(filenames):
        img = Image.open(path_to_input_images + filename)
        f = open(path_to_label + filename[:-4] + '.txt', "r")
        img = ImageOps.exif_transpose(img)
        #exif_data = img._getexif()

        w,h = img.size
        coord = np.zeros((1,5))
        for i, line in enumerate(f):
            l = line.split(' ')
            if i == 0:                      # This is for label txt files that consist of only one object
                coord[0,0] = l[1]
                coord[0,1] = l[2]
                coord[0,2] = l[3]
                coord[0,3] = l[4][:-1]
                coord[0,4] = l[0]
            else:                           # This is for label txt files that consist of more than one object
                coord = np.concatenate((coord, np.zeros((1,5))), axis=0)
                coord[i,0] = l[1]
                coord[i,1] = l[2]
                coord[i,2] = l[3]
                coord[i,3] = l[4][:-1]
                coord[i,4] = l[0]
            for m in range(coord.shape[0]): # Iterating over the array depending on the no. of lines/no. of objects
                if coord[m,2] > 0:
                    im1 = img.crop((w * coord[m, 0] - w * coord[m, 2] / 2,  #These calculations define
                                    h * coord[m, 1] - h * coord[m, 3] / 2,  #the corner points for the labels
                                    w * coord[m, 0] + w * coord[m, 2] / 2,
                                    h * coord[m, 1] + h * coord[m, 3] / 2
                                    ))
                    if coord[m,4] < 2:      # Only bounding boxes of type honeybee (0) and bumblebee (1) are extracted, no unknowns (2)
                        wcoord = str(coord[m, 0])
                        hcoord = str(coord[m, 1])
                        im1.save(export_dest_path + "/"
                                       + str(int(coord[m, 4])) + "_"
                                       + wcoord[:4] + "_"
                                       + hcoord[:4] + "_"
                                       + str(m) + "_"
                                       + filename[:-4] + ".jpg")
        if vis_bb_path is not None:
            is_drawn = False
            os.makedirs(vis_bb_path, exist_ok=True)
            img_draw = ImageDraw.Draw(img) 
            for m in range(coord.shape[0]):
                # draw the bb 
                x_min = w * coord[m, 0] - w * coord[m, 2] / 2
                x_max = w * coord[m, 0] + w * coord[m, 2] / 2
                y_min = h * coord[m, 1] - h * coord[m, 3] / 2
                y_max = h * coord[m, 1] + h * coord[m, 3] / 2
                rect = [x_min, y_min, x_max, y_max]
                # TODO make switch case lazy fucker
                if coord[m,4] == 0:
                    clr_str = "blue"
                if coord[m,4] == 1:
                    clr_str = "red"
                if coord[m,4] == 2:
                    clr_str = "yellow"
                img_draw.rectangle(rect, outline=clr_str, width=3)
                is_drawn = True
 
            if is_drawn:
                img.save(os.path.join(vis_bb_path, filename))

        # print("Coordinates:", coord)


if __name__ == '__main__':
    """
    tag = "2022_action_cam_day1"
    BB_snipper(f"/media/linn/export10tb/bees/dataset_final/datasets_by_days/{tag}/train/",
               f"/media/linn/export10tb/bees/dataset_final/datasets_by_days/{tag}/train/bee_snippets",
               f"/media/linn/export10tb/bees/dataset_final/datasets_by_days/{tag}/train/drawn_bb",
               )
    """
    # parent_dir = "/mnt/bee_cube/dataset_final/2021_2022_all_dataset_auged"
    parent_dir = "/mnt/bee_cube/dataset_final/actioncam_5days"
    BB_snipper(f"{parent_dir}/train/",
               f"{parent_dir}/train/bee_snippets",
     #          f"{parent_dir}/train/drawn_bb",
               )
