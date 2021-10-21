# Advent of Code - 2017 - day 8

input_data = open('d8_input.txt')
# input_data = open('d8_example.txt')

registers = list()
highest_value = int()


class Register:
    def __init__(self, name):
        self.name = name
        self.value = 0


def check_register(register, registers):
    """check if register is found in registers, if not create it!"""
    found = False
    for r in registers:
        if r.name == register:
            found = True
    if not found:
        # if not found, add the register!
        registers.append(Register(register))


def get_register_value(register, registers):
    """returns the value of the input register"""
    for r in registers:
        if r.name == register:
            return r.value
    return 0


def check_condition(condition, registers):
    check = False
    cur_value = get_register_value(condition[0], registers)
    op = condition[1]
    compare_value = int(condition[2])
    if op == '<':
        check = cur_value < compare_value
    elif op == '>':
        check = cur_value > compare_value
    elif op == '==':
        check = cur_value == compare_value
    elif op == '>=':
        check = cur_value >= compare_value
    elif op == '<=':
        check = cur_value <= compare_value
    elif op == '!=':
        check = cur_value != compare_value
    return check


def update_register(register, action, value, registers, highest_value):
    for r in registers:
        if r.name == register:
            if action == 'inc':
                r.value += value
            elif action == 'dec':
                r.value -= value
        if r.value > highest_value:
            highest_value = int(r.value)
    return highest_value


def get_largest_value(registers):
    max_value = int()
    for r in registers:
        if r.value > max_value:
            max_value = r.value
    return max_value


# Starts here
for instr in input_data:
    # print('\n ------------------------- \n instruction: ' + str(instr))
    reg = instr.split(' ')[0]
    act = instr.split(' ')[1]
    val = int(instr.split(' ')[2])
    condition = instr.split(' if ')[1].strip('\n').split(' ')
    # print(' reg      : ' + str(reg))
    # print(' action   : ' + str(act))
    # print(' val      : ' + str(val))
    # print(' condition: ' + str(condition))

    # check if register is found in registers, if not create it!
    check_register(reg, registers)
    check_register(condition[0], registers)

    # check if the condition is valid
    if check_condition(condition, registers):
        # perform the action
        # print('Condition is true! - ' + str(act) + 'reasing the register: ' + str(reg) + ' with value: ' + str(val))
        highest_value = update_register(reg, act, val, registers, highest_value)

input_data.close()
largest_value = get_largest_value(registers)

print(' Part one - the largest value in any register is: ' + str(largest_value))
print(' Part two - the highest value held in any register during this process is: ' + str(highest_value))
