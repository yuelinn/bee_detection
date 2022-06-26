import os
import numpy as np
import pandas as pd
from PIL import Image
path = "data/final_220526"
csv_name = "output_final_220526"

extended_path = (path + "/obj_train_data")
complete_df = pd.DataFrame()
print(complete_df)

#from PIL import Image
#def get_date_taken(path):
#    return Image.open(path)._getexif()
#print(get_date_taken(full_path))

path_name = list()
label = list()
coord_x = list()
coord_y = list()
size_x = list()
size_y = list()

for i in sorted(os.listdir(extended_path)):
    full_path = extended_path+"/"+i
    print(full_path)

    my_file = open(full_path, "r")
    #content = my_file.read()
    content = my_file.read().splitlines()
    if os.stat(full_path).st_size == -1: # ==0 -> empty files are also implemented in the dataframe
        path_name.append(i[:-4])
        label.append("")
        coord_x.append("")
        coord_y.append("")
        size_x.append("")
        size_y.append("")

    for l in content:
        print("Content:",content)
        splitted_content = l.split(" ")  # Split object
        path_name.append(i[:-4])
        label.append(splitted_content[0])
        coord_x.append(float(splitted_content[1]))
        coord_y.append(float(splitted_content[2]))
        #coord_y.append(float(splitted_content[2]))
        size_x.append(splitted_content[3])
        size_y.append(splitted_content[4])





print("List with all paths:",path_name," Länge:", len(path_name))
print("List with all labels:",label," Länge:", len(label))
print("List with all X Coords:",coord_x," Länge:", len(coord_x))
print("List with all Y Coords:",coord_y," Länge:", len(coord_y))
print("Es sind",len(path_name)," Objekte in der Liste")



df = pd.DataFrame(
    {'name':path_name,
     'label':label,
     'coord_x':coord_x,
     'coord_y':coord_y})

print(df)

df.to_csv("data/"+csv_name+".csv",index=False)