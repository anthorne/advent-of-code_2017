# Advent of Code - 2017 - day 9

the_input = open('d9_input.txt')

#  < >  - contains garbage
#  { }  - represents a group
#   !   - cancels the next character
# score - the outermost group gets 1 point, every nested level gets +1 points

score = 0
level = 0
inside_garbage = False
ignore_next = False

garbage = 0

for row in the_input:
    for c in row:
        if not ignore_next:
            if inside_garbage:
                if c != '>' and c != '!':
                    garbage += 1
            if c == '<':
                inside_garbage = True
            if not inside_garbage:
                if c == '{':
                    level += 1
                elif c == '}':
                    if level >= 1:
                        score += level
                        level -= 1
            else:
                if c == '>':
                    inside_garbage = False
            if c == '!':
                ignore_next = True
        else:
            ignore_next = False

the_input.close()

print(' Part one - the final score is: ' + str(score))
print(' Part two - the number of non-canceled characters within the garbage is: ' + str(garbage))
