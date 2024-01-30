import os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
import click
import yaml
from pathlib import Path
from matplotlib import font_manager
import random


@click.command()
@click.option(
    "--images_dir",
    type=str,
    help="path to the rgb directory",
    required=True,
)
@click.option(
    "--labels_dir",
    type=str,
    help="path to the labels directory",
    required=True,
)
@click.option(
    "--output_dir",
    type=str,
    help="path to the output directory",
    required=True,
)
@click.option(
    "--num_repeats",
    type=int,
    help="number of repeated random crops per bb.",
    required=True,
)
@click.option(
    "--patch_size",
    type=int,
    help="size of output image",
    required=True,
)
def crop_bbs(images_dir, labels_dir, output_dir, num_repeats, patch_size):
    """
    Function to draw bbs (from YOLO format txt labels) onto images
    Some parts were written by Julian Bauer
    """

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "labels"), exist_ok=True)

    filenames = os.listdir(images_dir)

    for filename in tqdm(filenames):
        try:
            img = Image.open(os.path.join(images_dir, filename))
        except:
            print(f"Skipping {filename} because PIL cannot read file as image.")

        f = open(os.path.join(labels_dir, Path(filename).stem + ".txt"), "r")
        img = ImageOps.exif_transpose(
            img
        )  # for smartphone images to be oriented correctly

        w, h = img.size
        coord = np.zeros((1, 5))
        for i, line in enumerate(f):
            l = line.split(" ")
            coord[0, 0] = l[1]
            coord[0, 1] = l[2]
            coord[0, 2] = l[3]
            coord[0, 3] = l[4][:-1]
            coord[0, 4] = l[0]

            # crop the image
            m = 0
            x_min = w * coord[m, 0] - w * coord[m, 2] / 2
            x_max = w * coord[m, 0] + w * coord[m, 2] / 2
            y_min = h * coord[m, 1] - h * coord[m, 3] / 2
            y_max = h * coord[m, 1] + h * coord[m, 3] / 2

            x_c = (x_max + x_min) / 2.
            y_c = (y_max + y_min) / 2.
            dw = x_max - x_min
            dh = y_max - y_min

            max_dx = int(round((patch_size - dw) / 2.))
            max_dy = int(round((patch_size - dh) / 2.))

            for n in range(num_repeats):
                dx_random = random.randint(-max_dx, max_dx+1)
                dy_random = random.randint(-max_dy, max_dy+1)

                new_x_c = int(x_c + dx_random)
                new_y_c = int(y_c + dy_random)

                new_x_min = int(round(new_x_c - (patch_size/2)))
                new_y_min = int(round(new_y_c - (patch_size/2)))
                new_x_min = max(new_x_min, 0)
                new_y_min = max(new_y_min, 0)

                
                # transform to new coords and normalise
                new_x = (new_x_c - new_x_min) / w
                new_y = (new_y_c - new_y_min) / h

                new_str = f"{l[0]} {new_x} {new_y} {float(l[3])*w/patch_size} {float(l[4])*h/patch_size}"
                new_filename = Path(filename).stem + f"_{new_x_c}_{new_y_c}_{patch_size}" + Path(filename).suffix

                new_x_max = new_x_min + patch_size
                new_y_max = new_y_min + patch_size
                # TODO make sure the crop does not go out of bounds on the max side

                new_rect = [new_x_min, new_y_min, new_x_max, new_y_max]
                import pdb; pdb.set_trace()
                img_cropped = img.crop(new_rect)
           
                img_cropped.save(os.path.join(output_dir, "images", new_filename))
                # save label txt 
                with open(os.path.join(output_dir, "labels", Path(new_filename).stem + ".txt"), "w") as new_label_f:
                    new_label_f.write(new_str)



if __name__ == "__main__":
    seed=2378
    random.seed(seed)
    np.random.seed(seed)
    # torch.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)
    crop_bbs()
