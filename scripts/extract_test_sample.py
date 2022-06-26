import numpy as np
import os
import shutil
import argparse

#parser = argparse.ArgumentParser( description='Extracting command line arguments', add_help=True )
#parser.add_argument( '--path', action='store', required=True )
#parser.add_argument( '--desired_amount', action='store', type=int, required=True )
#flags = parser.parse_args()



#origin_path = "/scratch/beestudents/220614/102_1406_clover"
#new_path = "/scratch/beestudents/220614/bee_clover/images/test"

origin_path = "data/102_1406_phacelias"
new_path = "data/test"

desired_amount = 50

amount_pictures = desired_amount//2
number_of_images = (len(os.listdir(origin_path)))
interval = number_of_images//amount_pictures


first_picture = sorted(os.listdir(origin_path))[0]
last_picture = sorted(os.listdir(origin_path))[number_of_images-2]

pre_first_digit = first_picture[:-4]
first_digit = int(pre_first_digit[-4:])

pre_last_digit = last_picture[:-4]
last_digit = int(pre_last_digit[-4:])

print(first_digit)
print(last_digit)

selection1 = list(range(first_digit, last_digit, interval))
selection2 = [x+1 for x in selection1]
print(selection1)
print(selection2)


for i in selection1:
    copy_from = origin_path + "/RIMG" + str(i)+".JPG"
    copy_to = new_path + "/RIMG" +str(i)+".JPG"
    shutil.copyfile(copy_from, copy_to)

for i in selection2:
        copy_from = origin_path + "/RIMG" + str(i) + ".JPG"
        copy_to = new_path + "/RIMG" + str(i) + ".JPG"
        shutil.copyfile(copy_from, copy_to)
