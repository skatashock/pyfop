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

# user's input for extension, label & context
input_extension = input('Extension number: ').strip()
input_label = input('Label: ').strip()
input_context = input('Context: ').strip()

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

# insert user's input extension to extension list in sorted order
bisect.insort_left(exts, input_extension)

input_data = [input_extension, '9999', input_label, input_context]
sips_data[input_extension] = input_data

for ext in exts:
    print('[SIP/{0}]'.format(sips_data[ext][0]))
    print('Position={0}'.format(sips_data[ext][1]))
    print('Label=\"{0}\"'.format(sips_data[ext][2]))
    print('Extension={0}'.format(sips_data[ext][0]))
    print('Context={0}'.format(sips_data[ext][3]))
    print('icon=1')
    print('\n')
