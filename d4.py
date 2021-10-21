file = open('d4_input.txt')

valid_partone = 0
valid_parttwo = 0
countRows = 0


def check_valid(words):
    valid_p1 = True
    valid_p2 = True
    if check_duplicates(words):
        # print('Duplicates found in passphrase!')
        valid_p1 = False
        valid_p2 = False
    if check_anagram(words):
        # print('Anagram found in passphrase!')
        valid_p2 = False
    return valid_p1, valid_p2


# --- Part one ---
def check_duplicates(words):
    found = False
    pos = 0
    for currentWord in words:
        check_pos = 0
        for checkWord in words:
            if currentWord == checkWord and pos != check_pos:
                found = True
                # print('Word: ' + str(currentWord) + ' is a duplicate! Array-pos: ' + str(pos) + ', ' + str(check_pos))
            check_pos += 1
        pos += 1
    return found


# --- Part two ---
def check_anagram(words):
    found = False
    pos = 0
    for current_word in words:
        check_pos = 0
        for check_word in words:
            if pos != check_pos:                                # compare only with other words in the array
                if len(current_word) == len(check_word):        # check only words with the same length
                    if sorted(current_word) == sorted(check_word):
                        found = True
                        # print('Found anagram in the words: ' + str(current_word) + ' and ' + str(check_word))
            check_pos += 1
        pos += 1
    return found


for row in file:
    countRows += 1
    words = row.strip().split(' ')
    # print(words)
    result = check_valid(words)
    if result[0]:
        valid_partone += 1
    if result[1]:
        valid_parttwo += 1


print('\n Part one: There are ' + str(valid_partone) + ' valid passphrases in a total of ' + str(countRows))
print(' Part two: There are ' + str(valid_parttwo) + ' valid passphrases in a total of ' + str(countRows))

