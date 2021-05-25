#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas

plt.plot([1, 2, 3, 4], [1, 4, 2, 3])

# %%
fig, axs = plt.subplots(2, 2)
# %%
a = pandas.DataFrame(np.random.rand(4, 5), columns=list('abcde'))
a_asarray = a.values

b = np.matrix([[1, 2], [3, 4]])
b_asarray = np.asarray(b)
print(type(b))
print(type(b_asarray))
# %%
x = np.linspace(0, 2, 100)
#%%
# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(x, x, label='linear')  # Plot some data on the axes.
ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.

# %%

