# theSet = set()
# theSet.add((("Small","Slow"), 0.4))
# theSet.add((("Small","Slow"), 0.5))
# theSet.add((("Small","Slow"), 0.4))
# theSet.add((("Small","Slow"), 0.4))
# print(theSet)
import numpy as np
from scipy.integrate  import quad
from fuzzy_logic import defuzzier, fuzzier

# coefficient = 0.9407208683835986
# x0 = 0.2 * coefficient + 0.4
# x1 = 0.8 - 0.2 * coefficient
#
# def fx(x):
#     if 0.4 <= x < x0:
#         return (x - 0.4) / 0.2
#     elif x0 <= x < x1:
#         return coefficient
#     elif x1 <= x < 0.8:
#         return (0.8 - x) / 0.2
#     else:
#         return 0.0
#
# def xfx(x):
#     if 0.4 <= x < x0:
#         return (x - 0.4) * x / 0.2
#     elif x0 <= x < x1:
#         return coefficient * x
#     elif x1 <= x < 0.8:
#         return (0.8 - x) * x / 0.2
#     else:
#         return 0.0
# result1, error1 = quad(fx, -15, 15, limit=100)
# result2, error2 = quad(xfx, -15, 15, limit = 100)

# print((result2, result1))
# x = -4.999999999652145
# y = defuzzier.defuzzify('Left', 0.9407208683835986, True)
# y = fuzzier.light_yellow(1, 0)
# print(y)
x = 0.6 - 0.5
print(x / 0.1)



