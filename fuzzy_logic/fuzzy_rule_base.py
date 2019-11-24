import xlrd


def read_deviation_rules():
    deviation_rules = []
    with xlrd.open_workbook('../fuzzy_logic/fuzzy_rule.xlsx') as book:
        sheet = book.sheet_by_index(0)
        deviation = [x for x in sheet.col_values(0)]
        steering = [y for y in sheet.col_values(1)]
        for i in range(1, len(deviation)):
            deviation_rules.append((deviation[i], steering[i]))
    return deviation_rules


def read_lights_rules():
    lights_rules = []
    with xlrd.open_workbook('../fuzzy_logic/fuzzy_rule.xlsx') as book:
        sheet = book.sheet_by_index(1)

        light_status = [y for y in sheet.col_values(0)]
        distance = [x for x in sheet.col_values(1)]
        deviation = [ z for z in sheet.col_values(2)]
        speed = [ t for t in sheet.col_values(3)]
        for i in range(1, sheet.nrows):
            lights_rules.append((light_status[i], distance[i], deviation[i], speed[i]))
    return lights_rules


def read_stones_rules():
    stones_rules = []
    with xlrd.open_workbook('../fuzzy_logic/fuzzy_rule.xlsx') as book:
        sheet = book.sheet_by_index(2)

        distance = [x for x in sheet.col_values(0)]
        deviation = [y for y in sheet.col_values(1)]
        speed = [z for z in sheet.col_values(2)]
        for i in range(1, sheet.nrows):
            stones_rules.append((distance[i], deviation[i], speed[i]))

    return stones_rules
