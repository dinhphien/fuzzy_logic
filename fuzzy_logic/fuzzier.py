# deviation membership functions:
# deviation in [0, 30]
from matplotlib import pyplot as plt
import numpy as np


def deviation_far_right(deviation):
    label = 'Far_left'
    degree = 0.0
    if 0 <= deviation <= 0.25:
        degree = 1.0
    elif 0.25 < deviation < 0.4:
        degree = (0.4 - deviation) / 0.15
    return label, degree


def deviation_right(deviation):
    label = 'Left'
    degree = 0.0
    if 0.25 <= deviation <= 0.4:
        degree = (deviation - 0.25) / 0.15
    elif 0.4 < deviation < 0.5:
        degree = (0.5 - deviation) / 0.1
    return label, degree


def deviation_middle(deviation):
    label = 'Middle'
    degree = 0.0
    if 0.4 <= deviation <= 0.5:
        degree = (deviation - 0.4) / 0.1
    elif 0.5 < deviation <= 0.6:
        degree = (0.6 - deviation) / 0.1
    return label, degree


def deviation_left(deviation):
    label = 'Right'
    degree = 0.0
    if 0.5 <= deviation <= 0.6:
        degree = (deviation - 0.5) / 0.1
    elif 0.6 < deviation <= 0.75:
        degree = (0.75 - deviation) / 0.15
    return label, degree


def deviation_far_left(deviation):
    label = 'Far_right'
    degree = 0.0
    if 0.6 <= deviation < 0.75:
        degree = (deviation - 0.6) / 0.15
    elif 0.75 <= deviation <= 1:
        degree = 1.0
    # print(degree)
    return label, degree


# steering membership functions:
# angle_steering in [-90, 90]


def steering_hard_right(angle):
    label = 'Hard_right'
    degree = 0.0
    if 5 < angle <= 10:
        degree = (angle - 5) / 5
    elif 10 < angle <= 15:
        degree = (15 - angle) / 5
    return label, degree


def steering_right(angle):
    label = 'Right'
    degree = 0.0
    if 0 < angle <= 5:
        degree = angle / 5
    elif 5 < angle <= 10:
        degree = (10 - angle) / 5
    return label, degree


def steering_straight(angle):
    label = 'Straight'
    degree = 0.0
    if -5 < angle <= 0:
        degree = (angle + 5) / 5
    elif 0 < angle <= 5:
        degree = (5 - angle) / 5
    return label, degree


def steering_left(angle):
    label = 'Left'
    degree = 0.0
    if -5 < angle <= 0:
        degree = -angle / 5
    elif -10 < angle <= -5:
        degree = (angle + 10) / 5
    return label, degree


def steering_hard_left(angle):
    label = 'Hard_left'
    degree = 0.0
    if -10 <= angle < -5:
        degree = (-angle - 5) / 5
    elif -15 < angle < -10:
        degree = (angle + 15) / 5
    return label, degree


# lights' status membership functions:

def light_green(time):
    label = 'Green'
    degree = 0.0
    if 0 <= time <= 4:
        degree = 1.0
    elif 4 < time <= 7:
        degree = (7 - time) / 3
    return label, degree


def light_less_green(time):
    label = 'Less_green'
    degree = 0.0
    if 4 <= time <= 7:
        degree = (time - 4) / 3
    elif 7 < time <= 10:
        degree = (10 - time) / 3
    return label, degree


def light_yellow(time):
    label = 'Yellow'
    degree = 0.0
    if 8 <= time <= 10:
        degree = (time - 8) / 2
    elif 10 < time <= 12:
        degree = 1.0
    elif 12 < time <= 15:
        degree = (15 - time) / 3
    return label, degree


def light_red(time):
    label = 'Red'
    degree = 0.0
    if 12 <= time <= 15:
        degree = (time - 12) / 3
    elif 15 < time <= 19:
        degree = 1.0
    elif 19 < time <= 22:
        degree = (22 - time) / 3
    return label, degree


def light_less_red(time):
    label = 'Less_red'
    degree = 0.0
    if 19 <= time <= 22:
        degree = (time - 19) / 3
    elif 22 < time <= 25:
        degree = 1.0
    return label, degree

# distance membership functions:


def distance_near(distance):
    label = 'Near'
    degree = 0.0
    if 0 <= distance <= 10:
        degree = 1.0
    elif 10 < distance < 30:
        degree = (30 - distance) / 20
    return label, degree


def distance_medium(distance):
    label = 'Medium'
    degree = 0.0
    if 20 <= distance < 50:
        degree = (distance - 20) / 30
    elif 50 <= distance < 80:
        degree = (80 - distance) / 30
    return label, degree


def distance_far(distance):
    label = 'Far'
    degree = 0.0
    if 75 <= distance < 100:
        degree = (distance - 75) / 25
    elif 100 <= distance:
        degree = 1.0
    return label, degree


# speed membership functions:


def speed_stop(speed):
    label = 'Stop'
    degree = 0.0
    if speed == 0:
        degree = 1.0
    elif 0 < speed <= 0.05:
        degree = (0.05 - speed) / 0.05
    return label, degree


def speed_slower(speed):
    label = 'Slower'
    degree = 0.0
    if 0 <= speed <= 0.3:
        degree = speed / 0.3
    elif 0.3 < speed <= 0.6:
        degree = (0.6 - speed) / 0.3
    return label, degree


def speed_slow(speed):
    label = 'Slow'
    degree = 0.0
    if 0.3 <= speed < 0.6:
        degree = (speed - 0.3) / 0.3
    elif 0.6 <= speed < 0.8:
        degree = (0.8 - speed) / 0.2
    return label, degree


def speed_medium(speed):
    label = 'Medium'
    degree = 0.0
    if 0.7 <= speed < 0.9:
        degree = (speed - 0.7) / 0.2
    elif 0.9 <= speed <= 1.0:
        degree = 1.0
    return label, degree


def read_membership_functions():
    membership_functions = {}
    membership_functions['deviation'] = [deviation_far_left, deviation_far_right, deviation_left, deviation_right,
                                         deviation_middle]
    membership_functions['steering'] = [steering_hard_left, steering_hard_right, steering_left, steering_right,
                                        steering_straight]
    membership_functions['light'] = [light_green, light_less_green, light_red, light_less_red, light_yellow]
    membership_functions['distance'] = [distance_far, distance_medium, distance_near]
    membership_functions['speed'] = [speed_medium, speed_slow, speed_slower, speed_stop]
    return membership_functions


# deviation:
# plt.figure(1)
# plt.xlabel("Deviation")
# plt.ylabel("Dependency")
#
# plt.title("Deviation dependency")
# plt.text(3, 1.0, "far_right")
# plt.text(8, 1.0, "right")
# plt.text(13, 1.0, "straight")
# plt.text(18, 1.0, "left")
# plt.text(23, 1.0, "far_left")
#
#
#
# dev_far_right = np.arange(0, 10, 0.1)
# dev_far_left = np.arange(20, 30, 0.1)
# dev_left = np.arange(15, 25, 0.1)
# dev_right = np.arange(5, 15, 0.1)
# dev_straight = np.arange(10, 20, 0.1)
#
# far_right = [deviation_far_right(x)[1] for x in dev_far_right]
# far_left = [deviation_far_left(x)[1] for x in dev_far_left]
# right = [deviation_right(x)[1] for x in dev_right]
# left = [deviation_left(x)[1] for x in dev_left]
# straight = [deviation_middle(x)[1] for x in dev_straight]
#
# plt.plot(dev_far_right, far_right, dev_far_left, far_left, dev_right, right, dev_left, left, dev_straight, straight)



# distance

# plt.figure(2)
# plt.xlabel("Distance")
# plt.ylabel("Dependency")
#
# plt.text(2, 1.0, "near")
# plt.text(50, 1.0, "medium")
# plt.text(120, 1.0, "far")
#
# plt.title("Distance dependency")
# dis_near = np.arange(0, 30, 0.1)
# dis_medium = np.arange(20, 80, 0.1)
# dis_far = np.arange(75, 150, 0.1)
#
# near = [distance_near(x)[1] for x in dis_near]
# medium = [distance_medium(x)[1] for x in dis_medium]
# far = [distance_far(x)[1] for x in dis_far]
# plt.plot(dis_near, near, dis_medium, medium, dis_far, far)


# light
# plt.figure(3)
# plt.xlabel("Time remaining")
# plt.ylabel("Dependency")
#
# plt.title("Light dependency")
# plt.text(1, 1.0, "less_green")
# plt.text(8, 1.0, "green")
# time_les_green = np.arange(0, 6, 0.1)
# time_green = np.arange(3, 15, 0.1)
#
# les_green = [light_less_green(0, x)[1] for x in time_les_green]
# green = [light_green(0, x)[1] for x in time_green]
# plt.plot(time_les_green, les_green, time_green, green)

# plt.show()

