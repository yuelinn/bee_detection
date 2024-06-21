#!/usr/bin/env python3
"""A script to get heatmap of where the insects were detected from the image and labels

"""

import os 
import sys

import numpy as np
import matplotlib
from matplotlib.image import NonUniformImage
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm

class BB_stats():
    def __init__(self):
        self.max_w = 0
        self.max_h = 0
        self.min_w = sys.float_info.max
        self.min_h = sys.float_info.max

        self.num = 0
        self.total_w = 0
        self.total_h = 0

    def update(self, w, h):
        self.max_w = max(self.max_w, w)
        self.max_h = max(self.max_h, h)
        self.min_w = min(self.min_w, w)
        self.min_h = min(self.min_h, h)
        self.total_w += w
        self.total_h += h
        self.num += 1

    def get_mean(self):
        mean_w = self.total_w / self.num
        mean_h = self.total_h / self.num
        return mean_w, mean_h

def get_heatmap(labels_dir):
    bb_stats = BB_stats()
    x_list = []
    y_list = []

    label_fns = os.listdir(labels_dir)

    for black_fn in BLACKLIST:
        try:
            label_fns.remove(black_fn)
        except:
            pass

    for fn in label_fns:
        fp = os.path.join(labels_dir, fn)
        f = open(fp, 'r')
        f_l = f.readlines()

        c_l = [int(obj.split()[0]) for obj in f_l]
        c_x = [float(obj.split()[1]) for obj in f_l]
        c_y = [float(obj.split()[2]) for obj in f_l]
        w_l = [float(obj.split()[3]) for obj in f_l]
        h_l = [float(obj.split()[4]) for obj in f_l]

        for w, h in zip(w_l, h_l):
            bb_stats.update(w, h)

        x_list.append(c_x)
        y_list.append(c_y)

    x_list = [x for xs in x_list for x in xs]
    y_list = [y for ys in y_list for y in ys]

    # histogram building
    # TODO make the bin size according to the bee size
    # TODO actually shouldnt the bins be the size of the flowers?
    xsteps=50
    xedges = np.linspace(0, 1.0, xsteps)
    ysteps = int(xsteps / 4608 * 3456)
    yedges = np.linspace(0, 1.0, ysteps)
    H, xedges, yedges = np.histogram2d(x_list, y_list, bins=(xedges, yedges))
    H = H.T

    cmap_plasma = plt.cm.get_cmap('plasma', 11)

    fig = plt.figure()
    neg = plt.imshow(H, interpolation='nearest', origin='upper',
                    extent=[xedges[0]*4608, xedges[-1]*4608, yedges[0]*3456, yedges[-1]*3456],
                    vmin=0,
                    vmax=10,
                    cmap=cmap_plasma)
    fig.colorbar(neg, location='right', anchor=(0, 0.3))
    plt.savefig(os.path.join(out_dir, date_treatment_str+"_heatmap.png"),  dpi=DPI)

    plt.close(fig)
    return H, xedges, yedges


def blur_map(heatmap):
    # FIXME
    return heatmap

def get_average_img(imgs_dir):
    imgs_fn_list = os.listdir(imgs_dir)

    # remove blacklisted images 
    for black_fn in BLACKLIST:
        try:
            imgs_fn_list.remove(black_fn.split(".")[0]+".JPG")
        except:
            pass
    
    num_imgs = len(imgs_fn_list)
    img_pil_dummy = Image.open(os.path.join(imgs_dir, imgs_fn_list[0]))
    img_np = np.zeros((img_pil_dummy.size[1], img_pil_dummy.size[0] , 3), dtype=float)
    for img_fn in tqdm(imgs_fn_list):
        img_pil = Image.open(os.path.join(imgs_dir, img_fn))
        img_np = img_np + np.asarray(img_pil).astype(float)

    return (img_np / num_imgs).astype(np.uint8)

def draw_heatmap(heatmap, xedges, yedges, imgs_dir, out_dir, date_treatment_str):
    ave_img = get_average_img(imgs_dir)
    Image.fromarray(ave_img.astype(np.uint8)).save(os.path.join(out_dir, date_treatment_str+"_ave.png"))
    
    fig = plt.figure()

    ax = fig.add_subplot(111, title='Locations where insects were detected')

    xedges = xedges * ave_img.shape[1]
    yedges = yedges * ave_img.shape[0]
    xcenters = (xedges[:-1] + xedges[1:]) / 2
    ycenters = (yedges[:-1] + yedges[1:]) / 2

    levels = np.linspace(0, 10, 11)
    # levels = np.linspace(heatmap.min(), heatmap.max(), 20)
    levels = levels[1:]

    cs = ax.contourf(xcenters, ycenters, heatmap, levels=levels, 
                alpha=0.5, 
                origin="upper", 
                extend='max', 
                # cmap="Wistia"
                # cmap="YlOrRd"
                # cmap = "autumn",
                # cmap="cividis",
                # cmap="inferno",
                cmap="plasma",
                # cmap="viridis",
                # cmap="RdYlGn_r",
                )

    """
    im = NonUniformImage(ax, interpolation='bilinear')
    xcenters = (xedges[:-1] + xedges[1:]) / 2
    ycenters = (yedges[:-1] + yedges[1:]) / 2
    import pdb; pdb.set_trace()
    im.set_data(ycenters, xcenters, heatmap)
    ax.images.append(im)
    # ax.set_aspect(0.75)
    """

    ax.imshow(ave_img, origin='upper')

    """
    plt.imshow(heatmap, interpolation='nearest', origin='lower',
                    extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], 
                    alpha=0.5,)
                    # cmap=matplotlib.colormaps["Reds"])
    """
    # plt.show()
    cbar = fig.colorbar(cs)
    plt.savefig(os.path.join(out_dir, date_treatment_str+"_heatmap_overlaid.png"),  dpi=DPI)
    plt.close(fig)

if __name__ == '__main__':
    parent_dir = "/mnt/mon13/bees/full_ds_after_r5_final/alles/"
    out_dir = "./heatmaps"

    # dates = ["220719"]
    # treatments = ["F", "F2"]

    dates = ["220710",  "220717",  "220719",  "220720","220721"]
    treatments = ["F", "PM", "P", "FM"]

    blacklist_fp = "blacklist_labels_fn.txt"  
    blacklist_f = open(blacklist_fp, "r")
    BLACKLIST = [x.strip() for x in blacklist_f.readlines()] # what, another global variable??!!

    DPI = 800
    # DPI = 1200

    for date_str in dates:
        for treatment_str in treatments:
            imgs_dir = os.path.join(parent_dir, date_str, treatment_str, "images")
            labels_dir = os.path.join(parent_dir, date_str, treatment_str, "labels")
            date_treatment_str = f"{date_str}_{treatment_str}"
            heatmap, xe, ye = get_heatmap(labels_dir)
            draw_heatmap(heatmap, xe, ye, imgs_dir, out_dir, date_treatment_str)
