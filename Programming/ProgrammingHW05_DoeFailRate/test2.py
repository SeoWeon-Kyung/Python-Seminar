import os
import re
from numpy.core.numeric import NaN
import pandas as pd

arr1 = pd.DataFrame({'Spec': [1, 2, 3, 4], 'Age': [18, 21, 34, 11], 'Grade': [87, 93, 45, 70]})
print(arr1)

arr2 = 60 < arr1['Grade']
print(arr2)

