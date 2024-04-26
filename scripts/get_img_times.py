# im still undecided if this is better done in bash or in python

import os
from PIL import Image, ExifTags



def str2secs(datetime_str):
    time_str = datetime_str.split()[1]
    time_l = time_str.split(":")
    h = int(time_l[0])
    m = int(time_l[1])
    s = int(time_l[2])

    secs = m  * 60 + h * 60 *60 + s
    return secs 

def one_plot(img_dir, plot_tagi, blacklist):
    img_fns = os.listdir(img_dir)
    img_fns = [ img_fn for img_fn in img_fns if plot_tag in img_fn ]

    # remove images of blaclist 
    for black_fn in blacklist:
        try:
            img_fns.remove(black_fn)
        except:
            pass

    img_fns.sort()

    # open first img
    first_img_fn = img_fns[0]
    first_img_pil = Image.open(os.path.join(img_dir, first_img_fn))
    img_exif = first_img_pil.getexif()

    for key, val in img_exif.items():
        if ExifTags.TAGS[key] == "DateTime":
            print(f'first img {first_img_fn} {ExifTags.TAGS[key]}:{val}', end=" ")
            break
    start_time = val

    # open last img
    first_img_fn = img_fns[-1]
    first_img_pil = Image.open(os.path.join(img_dir, first_img_fn))
    img_exif = first_img_pil.getexif()

    for key, val in img_exif.items():
        if ExifTags.TAGS[key] == "DateTime":
            print(f'last img {first_img_fn} {ExifTags.TAGS[key]}:{val}', end=" ")
            break
    end_time = val

    delta_time = str2secs(end_time) - str2secs(start_time)
    print(delta_time / 10)



if __name__ == "__main__":
    date_list = ["220710",  "220717",  "220719",  "220720", "220721"]
    plot_list = ["PM", "WF", "PH", "WM"]
    blacklist_fp = "blacklist_img_fn.txt"
    blacklist_f = open(blacklist_fp, "r")
    blacklist = [x.strip() for x in blacklist_f.readlines()]
    
    for date_tag in date_list:
        for plot_tag in plot_list:
            img_dir = f"/media/linn/export10tb/bees/dataset_old/cp_datasets/2022_action_cam/{date_tag}/images/"
            print(img_dir, plot_tag, end=" ")
            one_plot(img_dir, plot_tag, blacklist)

        print()




