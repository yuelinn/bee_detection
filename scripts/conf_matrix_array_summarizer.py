import numpy as np
import pandas as pd
import os

pd.options.display.max_columns = None
pd.options.display.max_rows = None

path = "data/tests_2023_pklnsort"

weights_result_dict = {}

array_name = ["honeybeeTP","bumblebeeTP","honeybeeFP","bumblebeeFP","honeybeeFN","honeybeeFN","TOTAL"]
for name in array_name:
    df_list = os.listdir((path + "/" + os.listdir(path)[0]))
    df = pd.DataFrame(columns=df_list)
    for i in os.listdir(path):
        new_row = []
        for j in os.listdir(path +"/" + i):
            array_path = path + "/" + i + "/" + j + "/" + "confusion_matrix_array.npy"
            array = np.load(array_path)
            array = np.nan_to_num(array)
            if name == "honeybeeTP":
                new_row.append(int([array[0,0]][0]))  # index for true positive honeybees (upper left corner in the cm)
            if name == "bumblebeeTP":
                new_row.append(int([array[1,1]][0])) # index for the true positive bumblebees ("center")

            if name == "honeybeeFP":
                new_row.append(int([array[0,3]][0]))  # index for false positive
            if name == "bumblebeeFP":
                new_row.append(int([array[1,3]][0]))  # index for false positive

            if name == "honeybeeFN":
                new_row.append(int([array[3, 0]][0]))  # index for false negative honeybees
            if name == "bumblebeeFN":
                new_row.append(int([array[3, 1]][0]))  # index for false negative bumblebees

            if name == "TOTAL":
                new_row.append(int(np.sum(array)))
                print(int(np.sum(array)))
        print(name,":")
        print(df)
        df = df.append(pd.Series(new_row, index=df_list, name=i))

    weights_result_dict[name] = df
    df.to_csv(name)

print(weights_result_dict)



