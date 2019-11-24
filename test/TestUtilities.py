# theSet = set()
# theSet.add((("Small","Slow"), 0.4))
# theSet.add((("Small","Slow"), 0.5))
# theSet.add((("Small","Slow"), 0.4))
# theSet.add((("Small","Slow"), 0.4))
# print(theSet)
import numpy as np
from scipy.integrate  import quad
def fx(x):
    coe = 0.8118558263232802
    x0 = 5 * coe - 5
    x1 = 5 - 5 * coe
    # print(x0, x1)
    if -5 < x <= x0:
        return (x + 5) / 5
    elif x0 < x <= x1:
        return coe
    elif x1 < x <= 5:
        return (5 - x) / 5
    else:
        return 0.0

def xfx(x):
    coe = 0.8118558263232802
    x0 = 5 * coe - 5
    x1 = 5 - 5 * coe
    # print(x0, x1)
    if -5 < x <= x0:
        return (x + 5) * x / 5
    elif x0 < x <= x1:
        return coe * x
    elif x1 < x <= 5:
        return (5 - x) * x / 5
    else:
        return 0.0
result= quad(fx, -15, 15, limit=100)
print(len(result))
print(result)
print(result[-1])
# space_x = np.arange(-15, 15, 0.01)
# y = [fx(x) for x in space_x]

# print(y)



