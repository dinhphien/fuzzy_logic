from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

# def get_implication_speed_stop(arg):
#     def speed_stop(speed):
#         label = 'Stop'
#         degree = 0.0
#         if speed == 0:
#             degree = 1.0
#         elif 0 < speed <= 0.1:
#             degree = (0.1 - speed) / 0.1
#         return label, degree
#
#
# def speed_slower(speed):
#     label = 'Slower'
#     degree = 0.0
#     if 0.1 < speed <= 0.3:
#         degree = (speed - 0.1) / 0.2
#     elif 0.3 < speed <= 0.5:
#         degree = (0.5 - speed) / 0.2
#     return label, degree
#
#
# def speed_slow(speed):
#     label = 'Slow'
#     degree = 0.0
#     if 0.4 <= speed < 0.6:
#         degree = (speed - 0.4) / 0.2
#     elif 0.6 <= speed < 0.8:
#         degree = (0.8 - speed) / 0.2
#     return label, degree
#
#
# def speed_medium(speed):
#     label = 'Medium'
#     degree = 0.0
#     if 0.7 <= speed < 0.9:
#         degree = (speed - 0.7) / 0.2
#     elif 0.9 <= speed <= 1.5:
#         degree = 1.0
#     return label, degree
#
#
# def steering_hard_right(angle):
#     label = 'Hard_right'
#     degree = 0.0
#     if 5 < angle <= 10:
#         degree = (angle - 5) / 5
#     elif 10 < angle <= 15:
#         degree = (15 - angle) / 5
#     return label, degree
#
#
# def steering_right(angle):
#     label = 'Right'
#     degree = 0.0
#     if 0 < angle <= 5:
#         degree = angle / 5
#     elif 5 < angle <= 10:
#         degree = (10 - angle) / 5
#     return label, degree
#
#
# def steering_straight(angle):
#     label = 'Straight'
#     degree = 0.0
#     if -5 < angle <= 0:
#         degree = (angle + 5) / 5
#     elif 0 < angle <= 5:
#         degree = (5 - angle) / 5
#     return label, degree
#
#
# def steering_left(angle):
#     label = 'Left'
#     degree = 0.0
#     if -5 < angle <= 0:
#         degree = -angle / 5
#     elif -10 < angle <= -5:
#         degree = (angle + 10) / 5
#     return label, degree
#
#
# def steering_hard_left(angle):
#     label = 'Hard_left'
#     degree = 0.0
#     if -10 <= angle < -5:
#         degree = (-angle - 5) / 5
#     elif -15 < angle < -10:
#         degree = (angle + 15) / 5
#     return label, degree

def defuzzify(Output_fuzzy_set, coefficient, flag):
    if flag:
        # steering:
        if Output_fuzzy_set == 'Hard_right':
            if coefficient == 1:
                def fx(x):
                    if 5 < x <= 10:
                        return (x - 5) / 5
                    elif 10 < x <= 15:
                        return (15 - x) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if 5 < x <= 10:
                        return (x - 5) * x / 5
                    elif 10 < x <= 15:
                        return (15 - x) * x / 5
                    else:
                        return 0.0

            else:
                x0 = 5 * coefficient + 5
                x1 = 15 - 5 * coefficient

                def fx(x):
                    if 5 < x <= x0:
                        return (x - 5) / 5
                    elif x0 < x <= x1:
                        return coefficient
                    elif x1 < x <= 15:
                        return (15 - x) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if 5 < x <= x0:
                        return (x - 5) * x / 5
                    elif x0 < x <= x1:
                        return coefficient * x
                    elif x1 < x <= 15:
                        return (15 - x) * x / 5
                    else:
                        return 0.0

        elif Output_fuzzy_set == 'Right':
            if coefficient == 1:
                def fx(x):
                    if 0 < x <= 5:
                        return x / 5
                    elif 5 < x <= 10:
                        return (10 - x) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if 0 < x <= 5:
                        return x * x / 5
                    elif 5 < x <= 10:
                        return (10 - x) * x / 5
                    else:
                        return 0.0
            else:
                x0 = 5 * coefficient
                x1 = 10 - 5 * coefficient

                def fx(x):
                    if 0 < x <= x0:
                        return x / 5
                    elif x0 < x <= x1:
                        return coefficient
                    elif x1 < x <= 10:
                        return (10 - x) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if 0 < x <= x0:
                        return x * x / 5
                    elif x0 < x <= x1:
                        return coefficient * x
                    elif x1 < x <= 10:
                        return (10 - x) * x / 5
                    else:
                        return 0.0

        elif Output_fuzzy_set == 'Straight':
            if coefficient == 1:
                def fx(x):
                    if -5 < x <= 0:
                        return (x + 5) / 5
                    elif 0 < x <= 5:
                        return (5 - x) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if -5 < x <= 0:
                        return (x + 5) * x / 5
                    elif 0 < x <= 5:
                        return (5 - x) * x / 5
                    else:
                        return 0.0

            else:
                x0 = 5 * coefficient - 5
                x1 = 5 - 5 * coefficient
                # print((x0, x1))


                def fx(x):
                    if -5 < x <= x0:
                        return (x + 5) / 5
                    elif x0 < x <= x1:
                        return coefficient
                    elif x1 < x <= 5:
                        return (5 - x) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if -5 < x <= x0:
                        return (x + 5) * x / 5
                    elif x0 < x <= x1:
                        return coefficient * x
                    elif x1 < x <= 5:
                        return (5 - x) * x / 5
                    else:
                        return 0.0

        elif Output_fuzzy_set == 'Left':
            if coefficient == 1:
                def fx(x):
                    if -10 < x <= -5:
                        return (x + 10) / 5
                    elif -5 < x <= 0:
                        return -x / 5
                    else:
                        return 0.0

                def xfx(x):
                    if -10 < x <= -5:
                        return (x + 10) * x/ 5
                    elif -5 < x <= 0:
                        return -x * x/ 5
                    else:
                        return 0.0

            else:
                x0 = 5 * coefficient - 10
                x1 = -5 * coefficient
                # print((x0, x1))

                def fx(x):
                    if -10 < x <= x0:
                        return (x + 10) / 5
                    elif x0 < x <= x1:
                        return coefficient
                    elif x1 < x <= 0:
                        return -x / 5
                    else:
                        return 0.0

                def xfx(x):
                    if -10 < x <= x0:
                        return (x + 10) * x / 5
                    elif x0 < x <= x1:
                        return coefficient * x
                    elif x1 < x <= 0:
                        return -x * x / 5
                    else:
                        return 0.0

        else:
            if coefficient == 1:
                def fx(x):
                    if -15 < x < -10:
                        return (x + 15) / 5
                    elif -10 <= x < -5:
                        return (-x - 5) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if -15 < x < -10:
                        return (x + 15) * x / 5
                    elif -10 <= x < -5:
                        return (-x - 5) * x / 5
                    else:
                        return 0.0

            else:
                x0 = 5 * coefficient - 15
                x1 = -(5 * coefficient + 5)

                def fx(x):
                    if -15 < x <= x0:
                        return (x + 15) / 5
                    elif x0 < x <= x1:
                        return coefficient
                    elif x1 < x <= -5:
                        return (-x - 5) / 5
                    else:
                        return 0.0

                def xfx(x):
                    if -15 < x <= x0:
                        return (x + 15) * x / 5
                    elif x0 < x <= x1:
                        return coefficient * x
                    elif x1 < x <= -5:
                        return (-x - 5) * x / 5
                    else:
                        return 0.0

        numerator, err1 = quad(xfx, -15, 15, limit=100)
        # numerator = 1
        # print(numerator)
        denominator, err2 = quad(fx, -15, 15, limit=100)
        # denominator = 1
        # print(denominator)
        # return fx
    else:
        # speed:
        if Output_fuzzy_set == 'Stop':
            if coefficient == 1:
                def fx(x):
                    if x == 0:
                        return 1.0
                    elif 0 < x <= 0.1:
                        return (0.1 - x) / 0.1
                    else:
                        return 0.0

                def xfx(x):
                    if x == 0:
                        return 1.0 * x
                    elif 0 < x <= 0.1:
                        return (0.1 - x) * x/ 0.1
                    else:
                        return 0.0
            else:
                x0 = 0.1 - 0.1 * coefficient

                def fx(x):
                    if x == 0:
                        return 1.0
                    elif 0< x <= x0:
                        return coefficient
                    elif x0 < x <= 0.1:
                        return (0.1 - x) / 0.1
                    else:
                        return 0.0

                def xfx(x):
                    if x == 0:
                        return 1.0 * x
                    elif 0 < x <= x0:
                        return coefficient * x
                    elif x0 < x <= 0.1:
                        return (0.1 - x) * x / 0.1
                    else:
                        return 0.0

        elif Output_fuzzy_set == 'Slower':
            if coefficient == 1:
                def fx(x):
                    if 0.1 < x <= 0.3:
                        return (x - 0.1) / 0.2
                    elif 0.3 < x <= 0.5:
                        return (0.5 - x) / 0.2
                    else:
                        return 0.0

                def xfx(x):
                    if 0.1 < x <= 0.3:
                        return (x - 0.1) * x / 0.2
                    elif 0.3 < x <= 0.5:
                        return (0.5 - x) * x / 0.2
                    else:
                        return 0.0

            else:
                x0 = 0.2 * coefficient + 0.1
                x1 = 0.5 - 0.2 * coefficient

                def fx(x):
                    if 0.1 < x <= x0:
                        return (x - 0.1) / 0.2
                    elif x0 < x <= x1:
                        return coefficient
                    elif x1 < x <= 0.5:
                        return (0.5 - x) / 0.2
                    else:
                        return 0.0

                def xfx(x):
                    if 0.1 < x <= x0:
                        return (x - 0.1) * x / 0.2
                    elif x0 < x <= x1:
                        return coefficient * x
                    elif x1 < x <= 0.5:
                        return (0.5 - x) * x / 0.2
                    else:
                        return 0.0

        elif Output_fuzzy_set == 'Slow':
            if coefficient == 1:
                def fx(x):
                    if 0.4 <= x < 0.6:
                        return (x - 0.4) / 0.2
                    elif 0.6 <= x < 0.8:
                        return (0.8 - x) / 0.2
                    else:
                        return 0.0

                def xfx(x):
                    if 0.4 <= x < 0.6:
                        return (x - 0.4) * x / 0.2
                    elif 0.6 <= x < 0.8:
                        return (0.8 - x)  * x / 0.2
                    else:
                        return 0.0

            else:
                x0 = 0.2 * coefficient + 0.4
                x1 = 0.8 - 0.2 * coefficient

                def fx(x):
                    if 0.4 <= x < x0:
                        return (x - 0.4) / 0.2
                    elif x0 <= x < x1:
                        return coefficient
                    elif x1 <= x < 0.8:
                        return (0.8 - x) / 0.2
                    else:
                        return 0.0

                def xfx(x):
                    if 0.4 <= x < x0:
                        return (x - 0.4) * x / 0.2
                    elif x0 <= x < x1:
                        return coefficient * x
                    elif x1 <= x < 0.8:
                        return (0.8 - x) * x / 0.2
                    else:
                        return 0.0

        else:
            if coefficient == 1:
                def fx(x):
                    if 0.7 <= x < 0.9:
                        return (x - 0.7) / 0.2
                    elif 0.9 <= x <= 1.5:
                        return 1.0
                    else:
                        return 0.0

                def xfx(x):
                    if 0.7 <= x < 0.9:
                        return (x - 0.7) * x / 0.2
                    elif 0.9 <= x <= 1.5:
                        return 1.0 * x
                    else:
                        return 0.0

            else:
                x0 = 0.2 * coefficient + 0.7

                def fx(x):
                    if 0.7 <= x < x0:
                        return (x - 0.7) / 0.2
                    elif x0 <= x <= 1.5:
                        return coefficient
                    else:
                        return 0.0

                def xfx(x):
                    if 0.7 <= x < x0:
                        return (x - 0.7) * x / 0.2
                    elif x0 <= x <= 1.5:
                        return coefficient * x
                    else:
                        return 0.0

        numerator, err1 = quad(xfx, 0, 1.5, limit=100)
        denominator, err2 = quad(fx, 0, 1.5, limit=100)
    crisp_value = numerator / denominator
    return crisp_value
    # return fx
# steering
# plt.figure(1)
# plt.xlabel("Steering")
# plt.ylabel("Dependency")
#
# plt.title("Steering dependency")
# plt.text(-10, 1.0, "hard_right")
# plt.text(-5, 1.0, "right")
# plt.text(0, 1.0, "straight")
# plt.text(5, 1.0, "left")
# plt.text(10, 1.0, "hard_left")
# labels_steering = ['Hard_right', 'Right', 'Straight', 'Left', 'Hard_left']
# space = np.arange(-15, 15, 0.1)
# dict_result = {}
# n = 0.1
# for label in labels_steering:
#     print(label)
#     fx = defuzzify(label, 1, True)
#     array_y = []
#     for x in space:
#         y = fx(x)
#         array_y.append(y)
#     dict_result[label] = array_y
#     n += 0.2
#
# plt.plot(space, dict_result['Hard_right'], space, dict_result['Right'], space, dict_result['Straight'], space, dict_result['Left'],
#          space, dict_result['Hard_left'])


# speed:
# plt.figure(2)
# plt.xlabel("Speed")
# plt.ylabel("Dependency")
#
# plt.title("Speed dependency")
# plt.text(0.1, 1.0, "Stop")
# plt.text(0.3, 1.0, "Slower")
# plt.text(0.6, 1.0, "Slow")
# plt.text(1.0, 1.0, "Medium")
# label_speeds = ["Stop", "Slower","Slow", "Medium"]
# space = np.arange(0, 1.5, 0.01)
# n = 0.1
# dict_result = {}
# for label in label_speeds:
#     print(label)
#     fx = defuzzify(label, 1, False)
#     array_y = []
#     for x in space:
#         y = fx(x)
#         array_y.append(y)
#     dict_result[label] = array_y
#     n += 0.2
#
# plt.plot(space[1:], dict_result['Stop'][1:], space, dict_result['Slower'], space, dict_result['Slow'], space, dict_result['Medium'])
# plt.show()


# result_left = defuzzify("Left", 0.1881441736767197, True)
# print(result_left)
# result_middle = defuzzify("Straight",0.8118558263232802, True)
