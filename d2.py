file_obj = open('d2_input.txt')

result = 0
for row in file_obj:
    c_large = 0
    c_small = 9999999999999
    cols = row.split('\t')
    for col in cols:
        if int(col) > int(c_large):
            c_large = int(col)
        if int(col) < c_small:
            c_small = int(col)
    result += c_large - c_small

print('Part 1 - result: ' + str(result))
file_obj.close()
file_obj = open('d2_input.txt')

result = 0
for row in file_obj:
    c_values = []
    c_sorted = []
    num_cols = -1
    cols = row.split('\t')
    for col in cols:
        num_cols += 1
        c_values.append(int(col))
        c_sorted.append(int(col))
    c_values.sort()
    c_sorted.sort()
    c_values.reverse()
    found = False
    for i in range(num_cols):
        for c in c_values:
            if (c_sorted[i] < c) and not found:
                if int(float(c / c_sorted[i]).is_integer()):
                    if not found:
                        result += int(c / c_sorted[i])
                        found = True
        num_cols -= 1

print('Part 2 - result: ' + str(result))        # 1040 is too high # 424 is too high # 286 is too low  # 333 is correct
file_obj.close()
