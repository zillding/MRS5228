import matplotlib.pyplot as plt
import numpy as np

total_number = 100
count = 0

x = np.linspace(0, 30, total_number)

array = []
path = r"D:\master study\cs5228 data mining\project\MRS5228\20151111-144411.log"
with open(path, "r") as ins:
    for line in ins:
        if count >= total_number:
            break;
        if 'So far, root mean square error:' in line:
            index = line.index('So far, root mean square error: ')
            array.append(line[index+32:-2])
            count = count + 1

plt.plot(x, array, label='k=5')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.tick_params(axis = 'x',
    which = 'both',
    bottom='off',
    top='off',
    labelbottom='off')

plt.show()