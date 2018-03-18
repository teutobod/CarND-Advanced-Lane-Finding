import numpy as np
#
# data = np.array([[1, 2, 3], [5, 6, 7]])
#
#
# print(np.average(data, axis=0))

class MovingAverage:
    def __init__(self, n_window):
        self.n_window = n_window
        self.list = []

    def add(self, x):

        if(len(self.list) >= self.n_window):
            self.list.pop(0)

        self.list.append(x)

        return np.average(np.array(self.list), axis=0)

ma = MovingAverage(3)

a = ma.add([1 ,2 ,3])
print(a)

a = ma.add([2 ,4 ,6])
print(a)

a = ma.add([1 ,2 ,3])
print(a)

print(a)

a = ma.add([1 ,2 ,3])
print(a)

a = ma.add([1 ,2 ,3])
print(a)