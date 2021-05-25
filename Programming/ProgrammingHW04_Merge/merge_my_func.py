# merge_my_func.py
# limit format csv file reader
import pandas as pd

def lim_data_read(path):
    data = pd.read_csv(path, header=2, index_col="barcode")
    data.drop_duplicates(keep='last', inplace=True)
    lim = pd.read_csv(path, names=data.columns, nrows=2)

    return data, lim