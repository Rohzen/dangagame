bottom = 0
top = 10

x = 0
y = 0

move_counter = 0
move_direction = 1

for c in range(50):
    y+=1 * move_direction

    if y==top:
        move_direction = -1

    if y==bottom:
        move_direction = 1

    print(str(y))
# for c in range(50):
    # y += move_direction
    # move_counter += 1
    # if abs(move_counter) > top:
        # move_direction *= -1
        # move_counter *= move_direction
    # print('>:' + str(y))