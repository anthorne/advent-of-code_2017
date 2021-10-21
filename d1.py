file_obj = open('d1_input.txt', 'r')

result = 0
prev_c = -1     # init value
file_rows = []
num_chars = 0

for row in file_obj:
    file_rows.append(row)
    for c in row:
        if c != '\n':
            num_chars += 1
            if prev_c != -1:
                if int(c) == prev_c:
                    result += int(c)
            prev_c = int(c)
result += int(c)

print('Part 1 - result: ' + str(result))

char_counter = 0
result = 0

for row in file_rows:
    for c in row:
        if c != '\n':
            if char_counter < (num_chars/2):
                index = int(int(char_counter) + (int(num_chars) / 2))
                if c == str(row[int(index)]):
                    result += (int(c) * 2)
            char_counter += 1

print('Part 2 - result: ' + str(result))

file_obj.close()