from fuzzy_logic import fuzzy_rule_base, fuzzier, defuzzier, fuzzy_inference_engine
from utils import config
import math
import numpy as np


def nor_deviation(dev):
    return dev / config.LANE_SIZE


def nor_time_light(status_light, time_remaining):
    if status_light == 0:
        return 10 - time_remaining
    elif status_light == 1:
        return 15 - time_remaining
    else:
        return 25 - time_remaining

class FuzzyController():
    def __init__(self):
        self.lights_rules = fuzzy_rule_base.read_lights_rules()
        self.stones_rules = fuzzy_rule_base.read_stones_rules()
        self.deviation_rules = fuzzy_rule_base.read_deviation_rules()
        self.membership_functions = fuzzier.read_membership_functions()

    def fuzzification(self, deviation, time, distance_light, distance_stone):
        # print((deviation, status_light, distance_light, remaining_time, distance_stone))
        dependencies = {}
        dev_dependency = []
        light_status_dependency = []
        light_dis_dependency = []
        stone_dis_dependency = []
        for dev_func in self.membership_functions['deviation']:
            label, degree = dev_func(deviation)
            if degree > 0.0:
                dev_dependency.append((label, degree))
        dependencies['deviation'] = dev_dependency

        for light_func in self.membership_functions['light']:
            label, degree = light_func(time)
            if degree > 0.0:
                light_status_dependency.append((label, degree))
        for dis_func in self.membership_functions['distance']:
            label, degree = dis_func(distance_light)
            if degree > 0.0:
                light_dis_dependency.append((label, degree))
        dependencies['status_light'] = light_status_dependency
        dependencies['distance_light'] = light_dis_dependency

        for dis_func in self.membership_functions['distance']:
            label, degree = dis_func(distance_stone)
            if degree > 0.0:
                stone_dis_dependency.append((label, degree))
        dependencies['distance_stone'] = stone_dis_dependency

        return dependencies

    def inference(self, dependencies):
        inferencies = {}
        light_infer = set()
        dev_infer = set()
        stone_infer = set()

        for fuzzified_dev in dependencies['deviation']:
            for dev_rule in self.deviation_rules:
                if fuzzified_dev[0] == dev_rule[0]:
                    dev_infer.add((dev_rule, fuzzified_dev[1]))
                    break
        inferencies['steering'] = dev_infer

        for fuzzified_status_light in dependencies['status_light']:
            for fuzzified_distance_light in dependencies['distance_light']:
                for fuzzified_dev in dependencies['deviation']:
                    for light_rule in self.lights_rules:
                        if light_rule[0] == '':
                            if fuzzified_distance_light[0] == light_rule[1] and fuzzified_dev[0] == light_rule[2]:
                                light_infer.add((light_rule, min((fuzzified_distance_light[1], fuzzified_dev[1]))))
                        elif light_rule[1] == '':
                            if fuzzified_status_light[0] == light_rule[0] and fuzzified_dev[0] == light_rule[2]:
                                light_infer.add((light_rule, min((fuzzified_status_light[1], fuzzified_dev[1]))))
                        elif light_rule[2] == '':
                            if fuzzified_status_light[0] == light_rule[0] and fuzzified_distance_light[0] == light_rule[1]:
                                light_infer.add((light_rule, min(fuzzified_status_light[1], fuzzified_distance_light[1])))
                        else:
                            if fuzzified_status_light[0] == light_rule[0] and fuzzified_distance_light[0] == light_rule[1] and fuzzified_dev[0] == light_rule[2]:
                                light_infer.add((light_rule, min((fuzzified_status_light[1], fuzzified_distance_light[1], fuzzified_dev[1]))))
        inferencies['light'] = light_infer

        for fuzzified_distance_stone in dependencies['distance_stone']:
            for fuzzified_dev in dependencies['deviation']:
                for stone_rule in self.stones_rules:
                    if stone_rule[1] == '':
                        if fuzzified_distance_stone[0] == stone_rule[0]:
                            stone_infer.add((stone_rule, fuzzified_distance_stone[1]))
                    elif fuzzified_distance_stone[0] == stone_rule[0] and fuzzified_dev[0] == stone_rule[1]:
                        stone_infer.add((stone_rule, min((fuzzified_distance_stone[1],fuzzified_dev[1]))))
        inferencies['stone'] = stone_infer

        return inferencies

    def defuzzification(self,consequents_args, flag):
        total_result = 0
        total_weight = 0
        result = 0
        de_rray = []
        if len(consequents_args) > 0:
            for consequent_arg in consequents_args:
                # print(consequent_arg[0][1])
                # print(consequent_arg[1])
                result_de = defuzzier.defuzzify(consequent_arg[0][-1], consequent_arg[1], flag)
                de_rray.append((consequent_arg,result_de))
                # print((consequent_arg, result))
                total_result += result_de * consequent_arg[1]
                total_weight += consequent_arg[1]
            result = total_result / total_weight
            return result, de_rray
        return float('nan'), float('nan')

    def control(self, deviation, status_light, distance_light, remaining_time, distance_stone, angle_deviation):
        normed_deviation = nor_deviation(deviation)
        time = nor_time_light(status_light, remaining_time)

        dependencies = self.fuzzification(normed_deviation, time, distance_light, distance_stone)

        inferences = self.inference(dependencies)
        # print(dependencies)
        # print(inferences)
        steering_angle, de_values_steering = self.defuzzification(inferences['steering'], True)
        print("////////////////////////////////////////////////////////////////////////////////////")
        print((deviation, status_light, distance_light, remaining_time, distance_stone))
        print(dependencies)
        print(inferences)
        speed_light_rule, de_values_speed = self.defuzzification(inferences['light'], False)
        print(("steering_angle: ", steering_angle))
        print(('defuzification_steering: ', de_values_steering))
        print(('speed: ', speed_light_rule))
        print(('defuzification_speed: ', de_values_speed))
        print(("angle_deviation: ", angle_deviation))
        # print(flag)
        print("//////////////////////////////////////////////////////////////////////////////////////")
        if len(inferences['stone']) > 0:
            # print("In stone fuzzy logic")
            # print("////////////////////////////////////////////////////////////////////////////////////")
            # print((deviation, status_light, distance_light, remaining_time, distance_stone))
            # print(dependencies)
            # print(inferences)
            speed_stone_rule, de_values_speed = self.defuzzification(inferences['stone'], False)
            # print(("steering_angle: ", steering_angle))
            # print(('defuzification_steering: ', de_values_steering))
            # print(('speed_light ', speed_light_rule))
            # print(('speed_stone', speed_stone_rule))
            # # print(('defuzification_speed: ', de_values_speed))
            # # print(("angle_deviation: ", angle_deviation))
            # # print(flag)
            # print("//////////////////////////////////////////////////////////////////////////////////////")
            return steering_angle, min(speed_stone_rule, speed_light_rule)
        return steering_angle, speed_light_rule





# fu = FuzzyController()
# dep = fu.control(14.059279131616401, 2 , 80, 0, 1000, 46)

