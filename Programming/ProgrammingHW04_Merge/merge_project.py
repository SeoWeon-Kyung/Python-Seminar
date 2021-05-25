#merge_project.py
import pandas as pd
import numpy as np
from merge_my_func import *

# Data read and Preprocessing
road = "../Python-Seminar/Programming/ProgrammingHW04_Merge"
a_data, a_lim = lim_data_read(road+"/a.csv")
b_data, b_lim = lim_data_read(road+"/b.csv")
c_data, c_lim = lim_data_read(road+"/c.csv")
# Merge three data
data = a_data.join(b_data)
data = data.join(c_data)
data["Spec"] = ""
# Merge limit info
lim = a_lim.join(b_lim).join(c_lim)
# Check spec out columns for every barcode
for col in data.columns[:-1]:
    temp = data[col].map(lambda p: \
        not(lim.loc["low limit", col] <= p <= lim.loc["high limit", col]))
    data.Spec[temp] += " " + str(col)
# Mark spec PASS data 
data["Spec"] = data["Spec"].replace("", "PASS")
# Data output as csv file  named "result.csv"
data.to_csv(road+"/result.csv")
    










