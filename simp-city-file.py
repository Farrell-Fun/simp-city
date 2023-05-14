#Fun Gao Wei, Farrell 
import random
import sys
import json


new_game_dict: dict
build_pos: str
chosen_building: str
high_score_list: list
options_input = ''
total = 0


# Create new dictionary of necessary parameter
def new_dict():
    global new_game_dict
    new_game_dict = {'building_list': ['HSE', 'FAC', 'SHP', 'HWY', 'BCH'], 'number_of_buildings': [8, 8, 8, 8, 8],
                     'points': 0,
                     'row_list': [1, 2, 3, 4], 'clm_list': ['A', 'B', 'C', 'D'], 'turn': 1,
                     'map_list': [['   ', '   ', '   ', '   '],
                                  ['   ', '   ', '   ', '   '],
                                  ['   ', '   ', '   ', '   '],
                                  ['   ', '   ', '   ', '   '],
                                  ],
                     'house_list': [], 'house_pos': [], 'shop_list': [], 'shop_pos': [],
                     'building_1': '', 'building_1_index': 0, 'building_2': '',
                     'building_2_index': 0}


# Function to select random buildings for every turn to be placed
def random_buildings():
    remaining_list = []
    for x in range(len(new_game_dict['building_list'])):
        if int(new_game_dict['number_of_buildings'][x]) != 0:
            remaining_list.append(new_game_dict['building_list'][x])
    new_game_dict['building_1'] = random.choice(remaining_list)
    new_game_dict['building_1_index'] = new_game_dict['building_list'].index(new_game_dict['building_1'])

    new_game_dict['building_2'] = random.choice(remaining_list)
    new_game_dict['building_2_index'] = new_game_dict['building_list'].index(new_game_dict['building_2'])


# Main function that increases the turn by one
def turn_advance():
    new_game_dict['turn'] += 1


# Function to display the map
def map_print_only(var):
    building_indices = 0
    plus_minus_lines = ''
    if var != 'final':
        print("Turn {}".format(new_game_dict['turn']))
    print('{:>5} {:>5} {:>5} {:>5}'.format('A', 'B', 'C', 'D'), end='')
    print('{:>15} {:>11}'.format('Building', 'Remaining'))
    for row in range(len(new_game_dict['map_list'])):
        plus_minus_lines = '+-----' * len(new_game_dict['map_list'][0]) + '+'
        if row == 0:
            print(' ' + plus_minus_lines, end = '')
            print('{:>12} {:>11}'.format('--------', '---------'))
        elif building_indices != 5:
            print(' ' + plus_minus_lines, end='')
            print('{:>9} {:9}'.format(new_game_dict['building_list'][building_indices], new_game_dict['number_of_buildings'][building_indices]))
            building_indices += 1
        else:
            print(' ' + plus_minus_lines)
        print(row + 1, end='')
        for clm in range(len(new_game_dict['map_list'][0])):
            vertical_bars = ('|' + ' ' + new_game_dict['map_list'][row][clm] + ' ')
            print(vertical_bars, end='')
        if building_indices != 5:
            print('|', end='')
            print('{:>9} {:9}'.format(new_game_dict['building_list'][building_indices], new_game_dict['number_of_buildings'][building_indices]))
            building_indices += 1
        else:
            print('|')
    print(' ' + plus_minus_lines)


# Displays the 5 options during game phase
def options():
    global options_input
    print('1. Build a {}'.format(new_game_dict['building_1']))
    print('2. Build a {}'.format(new_game_dict['building_2']))
    print('3. See current Score')
    print('')
    print('5. Save Game')
    print('0. Exit to main menu')
    options_input = input('Your choice? ')


# Main function for game progression, if turn 16 is finished, run the final sequence
def game_progression():
    global options_input
    while new_game_dict['turn'] != 17:
        map_print_only('Clear')
        options()
        if options_input.isdigit():
            options_input = int(options_input)
            if options_input == 1 or options_input == 2:
                building_to_be_placed(options_input)
                random_buildings()
                turn_advance()
            elif options_input == 3:
                showing_points()
            elif options_input == 5:
                saving_game()
                return None
            elif options_input == 0:
                return None
            else:
                print("Please enter a valid option\n")

        else:
            print("Please enter a digit as an option\n")

# final sequence
    print('Final layout of Simp City: \n')
    map_print_only('final')
    showing_points()
    print()
    high_score_checking(new_game_dict['points'])


# Function responsible for managing placement of chosen building on chosen location
def building_to_be_placed(options_input):
    global build_pos
    global chosen_building

    # While loop for input validation, last two elif not statements to validate if building position is placeable
    while True:
        build_pos = str(input("Build where? "))
        build_pos = build_pos.upper()

        if len(build_pos) != 2:
            print("Your building position must only contain 2 characters, Ex. A1/B2")

        elif build_pos[0] not in new_game_dict['clm_list']:
            print('Your Column character(Letter) is not valid!')

        elif int(build_pos[1]) not in new_game_dict['row_list']:
            print('Your Row character(number) is not valid!')

        elif not duplicate_building():
            print('You cannot build on an existing building!')

        elif not adjacent_blocks_check():
            print('You must build next to an existing building')

        else:
            break

    # Define whether the first option or second option was the chosen building
    if options_input == 1:
        chosen_building = new_game_dict['building_1']

    if options_input == 2:
        chosen_building = new_game_dict['building_2']

    # Next two if statements are to append house/shop positions for calculation
    if chosen_building == 'HSE':
        new_game_dict['house_pos'].append(build_pos)

    if chosen_building == 'SHP':
        new_game_dict['shop_pos'].append(build_pos)

    # Next two if statements to subtract a building from number_of_buildings as each building can only have 8 copies
    if options_input == 1:
        new_game_dict['number_of_buildings'][new_game_dict['building_1_index']] -= 1

    if options_input == 2:
        new_game_dict['number_of_buildings'][new_game_dict['building_2_index']] -= 1
    change_map_list(build_pos, chosen_building)


# Function to check for building on a position where a building already is
def duplicate_building():
    clm = new_game_dict['clm_list'].index(build_pos[0])
    row = int(build_pos[1]) - 1
    if new_game_dict['map_list'][row][clm] != '   ':
        return False
    else:
        return True


# Function to check if the building that is to be placed has a building adjacent to it
def adjacent_blocks_check():
    global left
    global right
    global above
    global below
    left = ''
    right = ''
    above = ''
    below = ''
    if new_game_dict['turn'] == 1:
        return True
    if int(ord(build_pos[0]) - 64) - 1 == 0:
        left = 'NA'
    else:
        left = str(new_game_dict['map_list'][int(build_pos[1]) - 1][int(ord(build_pos[0]) - 64) - 2])
    if int(ord(build_pos[0]) - 64) + 1 == 5:
        right = 'NA'
    else:
        right = str(new_game_dict['map_list'][int(build_pos[1]) - 1][int(ord(build_pos[0]) - 64)])
    if int(build_pos[1]) - 1 == 0:
        above = 'NA'
    else:
        above = str(new_game_dict['map_list'][int(build_pos[1]) - 2][int(ord(build_pos[0]) - 64) - 1])
    if int(build_pos[1]) + 1 == 5:
        below = 'NA'
    else:
        below = str(new_game_dict['map_list'][int(build_pos[1])][int(ord(build_pos[0]) - 64) - 1])

    if (left == 'NA' or left == '   ') and (right == 'NA' or right == '   ') and (above == 'NA' or above == '   ') and (
            below == 'NA' or below == '   '):
        return False
    else:
        return True


# Function responsible for placing building on chosen location
def change_map_list(build_pos, chosen_building):
    row = int(build_pos[1])
    clm = int(ord(build_pos[0]) - 64)
    new_game_dict['map_list'][row - 1][clm - 1] = chosen_building


# Function to create the display for points (Ex. HSE: 0)
def calculations_display(x):
    sum_all = 0  # int for the total of scores for each building type
    temp = ''  # temp is a str which is the numbers to be printed, Ex. 0 or 1 + 3 + 1 = 5
    for y in range(len(building_points[x])):
        sum_all += int(building_points[x][y])
    for z in range(len(building_points[x])):
        if z == len(building_points[x]) - 1:
            temp += str(building_points[x][z]) + ' '
            break
        temp += str(building_points[x][z]) + ' + '
    temp += str('= ' + str(sum_all))
    if sum_all == 0:
        temp = '0'
    print(temp)
    return sum_all


# Function which loops calculation_display function to print out the whole points orderly
def showing_points():
    global building_points
    total = 0
    building_points = [[], [], [], [], []]
    beach_calculation()
    factory_calculation()
    house_calculation()
    shop_calculation()
    highway_calculation()
    for x in range(len(new_game_dict['building_list'])):
        # print is to print HSE: or BCH:
        print(new_game_dict['building_list'][x] + ': ', end='')
        total += calculations_display(x)
        # Total is an int for the sub total to be printed later, and calculation display in above line prints the
        # calculation of points
        new_game_dict['points'] = total
    print("Total Points: {}".format(total))


# Next 6 functions are for calculation of respective buildings
def beach_calculation():
    for x in range(len(new_game_dict['map_list'])):
        for y in range(len(new_game_dict['map_list'][0])):
            if 'BCH' in new_game_dict['map_list'][x][y] and (y == 0 or y == 3):  # If column is A or D, BCH scores 3 pts
                building_points[4].append('3')
            elif 'BCH' in new_game_dict['map_list'][x][y] and (y == 1 or y == 2):
                building_points[4].append('1')


def factory_calculation():
    factory_num = int(8 - int(new_game_dict['number_of_buildings'][1]))
    #  Subtracting 8 from remaining factories gets the number of factories on the board
    if factory_num <= 4:
        for x in range(0, factory_num):
            building_points[1].append(factory_num)
    else:
        for x in range(0, 4):
            building_points[1].append(4)
        for x in range(4, factory_num):
            building_points[1].append(1)


def house_calculation():
    temp_append = 0
    for x in range(len(new_game_dict['house_pos'])):
        adjacent_building(new_game_dict['house_pos'][x], 'HSE')
        for y in range(len(new_game_dict['house_list'][x])):
            if new_game_dict['house_list'][x][y] == 'FAC':
                building_points[0].append(1)
                temp_append = 0
                break  # Break statement as if there is a factory adjacent to a house, it can only score 1 point
            if new_game_dict['house_list'][x][y] == 'HSE' or new_game_dict['house_list'][x][y] == 'SHP':
                temp_append += 1
            if new_game_dict['house_list'][x][y] == 'BCH':
                temp_append += 2
        if temp_append == 0:
            continue
        building_points[0].append(temp_append)
        temp_append = 0


# Function to append to adjacent buildings of house/shop_list for calculation, NA refers to an invalid space
def adjacent_building(build_pos, chosen_building):
    if int(ord(build_pos[0]) - 64) - 1 == 0:
        left = 'NA'
    else:
        left = str(new_game_dict['map_list'][int(build_pos[1]) - 1][int(ord(build_pos[0]) - 64) - 2])
    if int(ord(build_pos[0]) - 64) + 1 == 5:
        right = 'NA'
    else:
        right = str(new_game_dict['map_list'][int(build_pos[1]) - 1][int(ord(build_pos[0]) - 64)])
    if int(build_pos[1]) - 1 == 0:
        above = 'NA'
    else:
        above = str(new_game_dict['map_list'][int(build_pos[1]) - 2][int(ord(build_pos[0]) - 64) - 1])
    if int(build_pos[1]) + 1 == 5:
        below = 'NA'
    else:
        below = str(new_game_dict['map_list'][int(build_pos[1])][int(ord(build_pos[0]) - 64) - 1])

    if chosen_building == 'HSE':
        new_game_dict['house_list'].append([build_pos, left, right, above, below])
    elif chosen_building == 'SHP':
        new_game_dict['shop_list'].append([build_pos, left, right, above, below])


def shop_calculation():
    dupe_list = []  # dupe_list will store the adjacent buildings that have been checked, therefore finding no. of
    # exclusive buildings adjacent to shop
    for x in range(len(new_game_dict['shop_pos'])):
        adjacent_building(new_game_dict['shop_pos'][x], 'SHP')
        dupe_list = []
        for y in range(1, len(new_game_dict['shop_list'][x])):
            if new_game_dict['shop_list'][x][y] == '   ' or new_game_dict['shop_list'][x][y] == 'NA':
                continue
            if new_game_dict['shop_list'][x][y] not in dupe_list:
                dupe_list.append(new_game_dict['shop_list'][x][y])
        building_points[2].append(len(dupe_list))


def highway_calculation():
    count = 0  # count is used as a counter for the number of highways in the current row
    rows = []
    for x in range(len(new_game_dict['map_list'])):
        rows.append(new_game_dict['map_list'][x])  # Appends the individual rows and the buildings in it
        for y in range(len(new_game_dict['map_list'][x])):

            if y + 1 == len(new_game_dict['map_list'][x]) and rows[x][y] == 'HWY':
                # condition if HWY is the last in the row
                count += 1
                building_points[3].extend([count] * count)

                count = 0
                continue

            if y + 1 == len(new_game_dict['map_list'][x]):
                # condition if the last item in the row has been reached
                building_points[3].extend([count] * count)

                count = 0
                continue

            if rows[x][y] == 'HWY' and rows[x][y + 1] != 'HWY':
                # condition if the next building on the right of an highway is NOT a HWY
                count += 1
                building_points[3].extend([count] * count)

                count = 0
                continue

            if rows[x][y] == 'HWY' and rows[x][y + 1] == 'HWY':
                # condition if the next building to the right of an highway IS a HWY
                count += 1

        if count == 0:
            continue


# Function to save game using json
def saving_game():
    file = open('save.txt', 'w+')
    data = json.dumps(new_game_dict)
    # JSON, JavaScript Object Notation used to store dictionary as txt and csv are incapable of storing lists as they
    # are stored as strings.
    file.write(data)
    file.close()
    print('Game Saved!')


# Function to load save game using json
def load_game():
    global new_game_dict
    file = open('save.txt', 'r')
    temp_data = file.readline()
    new_game_dict = json.loads(temp_data)
    file.close()


# 'Main' function for checking for high score
def high_score_checking(total_score):
    if high_score_pos_check(total_score) != 'poor':
        print('Congratulations! You made the high score board at position {}!'.format(high_score_pos_check(total_score)))
        name = str(input('Please enter your name (max 20 chars): '))
        high_score_extraction_appending(total_score, name)
        show_high_score()
    else:
        print('Your score did not make it to the leaderboard. Better luck next time!')
        return None


# Function to check if the score made it to the leaderboard
def high_score_pos_check(total_score):
    data_file = open('high_score.txt', 'r')
    data_file.seek(0)
    temp_data = data_file.readline()
    if len(temp_data) == 0:
        return 1
    score_list = json.loads(temp_data)
    data_file.close()

    for x in range(len(score_list)):
        if total_score >= int(score_list[x][1]):
            x += 1
            return x
    if len(score_list) != 10:
        return len(score_list) + 1
    # Return 'poor' means that the score did not make it to the leaderboard
    return 'poor'


# Function to manage the appending of the current high score the the high score list
def high_score_extraction_appending(total_score, name):
    global high_score_list
    data_file = open('high_score.txt', 'r')
    data_file.seek(0)
    temp_data = data_file.readline()

    # this condition is to manage if the high score board is empty
    if len(temp_data) == 0:
        # total_score == 'Pass' only occurs if the user is accessing the high score from the main menu
        if total_score == 'Pass':
            print('There is no High Score list yet...')
            return
        high_score_list = []
        high_score_list.append([name, total_score])
        data_file = open('high_score.txt', 'w+')
        data = json.dumps(high_score_list)
        data_file.write(data)
        data_file.close()
        return
    else:
        high_score_list = json.loads(temp_data)
        if total_score == 'Pass':
            show_high_score()
            return None
    data_file.close()
    for x in range(len(high_score_list)):
        if len(high_score_list) != 10:
            if total_score <= int(high_score_list[len(high_score_list) - 1][1]):
                high_score_list.append([name, total_score])
                data_file = open('high_score.txt', 'w')
                data = json.dumps(high_score_list)
                data_file.write(data)
                data_file.close()
                return x

        if total_score >= int(high_score_list[x][1]):
            high_score_list.insert(x, [name, total_score])
            high_score_list = high_score_list[0:10]
            data_file = open('high_score.txt', 'w')
            data = json.dumps(high_score_list)
            data_file.write(data)
            data_file.close()
            return x


# Function to display the high score
def show_high_score():
    print()
    print('--------- HIGH SCORES ---------')
    print('{:<4}{:<22}{:<5}'.format('Pos', 'Player', 'Score'))
    print('{:<4}{:<22}{:<5}'.format('---', '------', '-----'))
    for x in range(len(high_score_list)):
        player = high_score_list[x][0]
        score = high_score_list[x][1]
        print('{:>2}. {:<20}{:>7}'.format(x+1, player, score))


# Funtion for the startup sequence
def main():
    main_menu_input = input("Welcome, mayor of Simp City!\n"
                            "----------------------------\n"
                            "1. Start new game\n"
                            "2. Load saved game\n"
                            "3. Show High Scores\n"
                            "\n"
                            "0. Exit\n"
                            "Your Choice? ")
    if main_menu_input.isdigit():
        main_menu_input = int(main_menu_input)
        if main_menu_input == 1:
            new_dict()
            random_buildings()
            game_progression()
        elif main_menu_input == 2:
            load_game()
            game_progression()
        elif main_menu_input == 3:
            high_score_extraction_appending('Pass', 'Pass')
            return
        elif main_menu_input == 0:
            sys.exit()
        else:
            print('Please enter a valid option\n')
            return
    else:
        print('Please enter a digit\n')
        return


while True:
    main()
