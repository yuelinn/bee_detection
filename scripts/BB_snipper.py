import os
from PIL import Image
import numpy as np

def BB_snipper(label_root_path, export_dest_path):
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

    path_to_input_images = label_root_path+"/images/"
    path_to_label = label_root_path+"/labels/"
    filenames = os.listdir(path_to_input_images)
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')


    for j,filename in enumerate(filenames):
        img = Image.open(path_to_input_images + filename)
        f = open(path_to_label + filename[:-4] + '.txt', "r")
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
        print("Coordinates:", coord)


BB_snipper("data","export")
