
from copy import deepcopy

x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
y = deepcopy(x)
print([id(i) for i in x])
print([id(i) for i in y])

def show(x):
    for i in x:
        print(i)

for i in range(3):
    for j in range(3):
        print("before y")
        show(y)
        print("x")
        show(x)
        y[j][2-i] = x[i][j]
        print("after y")
        show(y)
        print("x")
        show(x)


print("final y~")
show(y)
print("x")
show(x)


