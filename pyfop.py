import sys
import re
import bisect

# Sample data:
# [Sip/2003]
# Position=17
# Label="2003 B.S"
# Extension=2003
# Context=internal-mas
# icon=1

# regex pattern
sip_regex = re.compile(r'''(
    ((;?)\[SIP/(\d{2,4})\])\n   # 1: line, 2: commented, 3: ext. number
    (Position=(\d{1,3}))\n      # 4: line, 5: position
    (Label="(.*)")\n            # 6: line, 7: label
    (Extension=(\d{2,4}))\n     # 8: line, 9: ext. number
    (Context=(.*))\n            # 10: line, 11: context
    (Icon=(\d+))\n              # 12: line, 13: icon
    )''', re.IGNORECASE | re.VERBOSE)

# open, copy content & close config file
config_file = open('./op_buttons.cfg')
config = config_file.read()
config_file.close()

# find all matching pattern from config file content
results = sip_regex.findall(config)
exts = []       # extension list variable
positions = []  # position list variable
sips_data = {}  # sips data dictionary variable

# iterate over each regex results
for result in results:
    # make sure it's not commented
    if not result[2]:
        # define variables
        extension = result[3]   # extension
        position = result[5]    # position
        label = result[7]       # label
        context = result[11]    # context

        # add extension to extension list
        exts.append(extension)
        # add position to position list
        positions.append(position)

        # create list of data needed per extension
        extension_data = [extension, position, label, context]
        # add above list to sips dictionary
        sips_data[extension] = extension_data

# get input for Extension Number & some validation
while True:
    try:
        # make sure the input is an integer
        input_extension = int(input('Extension number: ').strip())
        # check if the input number already exists
        if str(input_extension) not in exts:
            break
        else:
            print('The Extension number exists. Try again ...')
    except ValueError:
        print('Oops!  That was not a valid number.  Try again...')

# get input for Label & some validation
while True:
    input_label = input('Label: ').strip()
    # make sure input is not empty
    if input_label:
        break
    else:
        print('Please enter a Label value. Try again ...')

# get input for Context & some validation
while True:
    input_context = input('Context: ').strip()
    # make sure input is not empty
    if input_label:
        break
    else:
        print('Please enter a Context value. Try again ...')

# get last extension
exts_last = int(exts[-1])

# get sip last position value, convert to int
exts_last_position = int(sips_data[str(exts_last)][1])

# add +1 to exts_new last position value
exts_new_last_position = exts_last_position + 1

# copy old exts to exts_new
# we need before and after exts later
exts_new = exts.copy()

# insert user's input extension to exts_new in sorted order
bisect.insort_left(exts_new, str(input_extension))

# if input extension less than currently last extension
if exts_last > input_extension:
    # find input_extension index number in exts_new list
    input_extension_index = exts_new.index(str(input_extension))

    # next sip positions after inserted
    next_positions = []

    # iterate from input_extension index to exts last index
    for i in range(input_extension_index, len(exts)):
        # add sip position to next_positions list
        next_positions.append(sips_data[exts[i]][1])

    # add to next_positions list, convert back to string
    next_positions.append(str(exts_new_last_position))

    # create list of new input data, including new position
    # then add to sips_data
    input_data = [str(input_extension),
                  next_positions[0],
                  input_label,
                  input_context]

    sips_data[str(input_extension)] = input_data

    # remove first index from next_positions
    next_positions.pop(0)

    n = 0  # set initial n value to 0

    # iterate from after input_extension index to exts_new last index
    for i in range((input_extension_index + 1), len(exts_new)):
        # update all sips position after
        sips_data[exts_new[i]][1] = next_positions[n]
        n += 1  # n = n + 1

# else if input extension greater than currently last extension
else:
    # create list of new input data, including new position
    # then add to sips_data
    input_data = [str(input_extension),
                  exts_new_last_position,
                  input_label,
                  input_context]

    sips_data[str(input_extension)] = input_data

for ext in exts_new:
    print('[SIP/{0}]'.format(sips_data[ext][0]))
    print('Position={0}'.format(sips_data[ext][1]))
    print('Label=\"{0}\"'.format(sips_data[ext][2]))
    print('Extension={0}'.format(sips_data[ext][0]))
    print('Context={0}'.format(sips_data[ext][3]))
    print('icon=1')
    print('\n')
