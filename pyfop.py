#!/usr/bin/env python

import sys
import re
import bisect
import os

# Sample data:
# [Sip/2003]
# Position=17
# Label="2003 B.S"
# Extension=2003
# Context=internal-mas
# icon=1

# Config filename
config_filename = 'op_buttons.cfg'
config_filename_temp = 'op_buttons.cfg.tmp'

# Extensions list, default to empty list
exts = []

# Positions list, default to empty list
positions = []

# Extension numbers range between 2000 and 3999
ext_start = 2000
ext_end = 3999


# Copy others configs
def find_header(config):
    # Regex pattern
    header_regex = re.compile(r';START([\s\S]+);END')
    result = header_regex.search(config)
    return result


# Open, copy content and close config file
def read_config(filepath):
    config_file = open(filepath)
    config = config_file.read()
    config_file.close()
    return config


# Find all sips function
def sip_findall(config):
    # Sips data dictionary
    sips_data = {}

    # Regex pattern
    sip_regex = re.compile(r'''(
        ((;?)\[SIP/(2\d{3}|3[0-2]\d{2})\])\n # 1:line, 3:ext. number
        (Position=(\d{1,3}))\n      # 4:line, 5:position
        (Label="(.*)")\n            # 6:line, 7:label
        (Extension=(\d{2,4}))\n     # 8:line, 9:ext. number
        (Context=(.*))\n            # 10:line, 11:context
        (Icon=(\d+))                # 12:line, 13:icon
        )''', re.IGNORECASE | re.VERBOSE)

    # Find all matching pattern
    results = sip_regex.findall(config)

    # Iterate over each regex results
    for result in results:
        # Make sure it's not commented
        if not result[2]:
            # Define variables
            extension = result[3]   # extension
            position = result[5]    # position
            label = result[7]       # label
            context = result[11]    # context

            # Add extension to extension list
            exts.append(extension)

            # Add position to position list
            positions.append(position)

            # Create list of data needed per extension
            extension_data = [extension, position, label, context]
            # Add above list to sips dictionary
            sips_data[extension] = extension_data

    return sips_data


# Find sip by extension number
def sip_findone(config, ext):
    # Regex pattern
    sip_regex = re.compile(r'''(
        ((;?)\[SIP/%s])\n # 1:line, 3:ext. number
        (Position=(\d{1,3}))\n      # 4:line, 5:position
        (Label="(.*)")\n            # 6:line, 7:label
        (Extension=(\d{2,4}))\n     # 8:line, 9:ext. number
        (Context=(.*))\n            # 10:line, 11:context
        (Icon=(\d+))\n              # 12:line, 13:icon
        )''' % (ext), re.IGNORECASE | re.VERBOSE)

    # Find matching pattern
    results = sip_regex.findall(config)

    # Return the result if matched
    return results


# Write/update sips data to config file
def write_config(config, exts_new, sips_data):
    with open(config_filename_temp, 'w') as testfile:
        header = find_header(config)
        testfile.write(header.group())
        testfile.write('\n\n')
        if header:
            for ext in exts_new:
                testfile.write('[SIP/{0}]\n'.format(sips_data[ext][0]))
                testfile.write('Position={0}\n'.format(sips_data[ext][1]))
                testfile.write('Label=\"{0}\"\n'.format(sips_data[ext][2]))
                testfile.write('Extension={0}\n'.format(sips_data[ext][0]))
                testfile.write('Context={0}\n'.format(sips_data[ext][3]))
                testfile.write('icon=1\n\n')
        else:
            print('Header template missing. Action aborted.')
            sys.exit()

    os.rename(config_filename_temp, config_filename)


# Delete sips data from config file
def del_config(exts_new, sips_data):
    with open(config_filename_temp, 'w') as testfile:
        header = find_header(config)
        testfile.write(header.group())
        testfile.write('\n\n')
        if header:
            for num, ext in enumerate(exts_new, start=0):
                testfile.write('[SIP/{0}]\n'.format(sips_data[ext][0]))
                testfile.write('Position={0}\n'.format(positions[num]))
                testfile.write('Label=\"{0}\"\n'.format(sips_data[ext][2]))
                testfile.write('Extension={0}\n'.format(sips_data[ext][0]))
                testfile.write('Context={0}\n'.format(sips_data[ext][3]))
                testfile.write('icon=1\n\n')
        else:
            print('Header template missing. Action aborted.')
            sys.exit()

    os.rename(config_filename_temp, config_filename)


# Config file
config = read_config(config_filename)

# Check action and extension number argument/parameter
if len(sys.argv) == 3:
    # Make sure extension number is integer
    try:
        input_extension = int(sys.argv[2])
    except ValueError:
        print('Oops! That was not a valid extension number. Exiting.')
        sys.exit()

    # Limit extension number between 2000 and 3999
    if input_extension < ext_start or input_extension > ext_end:
        print('Extension number must be between 2000 and 3999. Exiting.')
        sys.exit()

    # Add new extension
    if sys.argv[1] == 'add':
        # Get sips data
        sips_data = sip_findall(config)

        # Check if the input number already exists
        if str(input_extension) in exts:
            print('That extension number exists. Exiting.')
            sys.exit()

        # Get input for Label & some validation
        while True:
            input_label = input('Label: ').strip()
            # Make sure input is not empty
            if input_label:
                break
            else:
                print('Please enter a Label value. Try again ...')

        # Get input for Context & some validation
        while True:
            input_context = input('Context: ').strip()
            # Make sure input is not empty
            if input_context:
                break
            else:
                print('Please enter a Context value. Try again ...')

        # Get last extension
        exts_last = int(exts[-1])

        # Get sip last position value, convert to int
        exts_last_position = int(sips_data[str(exts_last)][1])

        # Add +1 to exts_new last position value
        exts_new_last_position = exts_last_position + 1

        # Copy old exts to exts_new
        # We'll need before and after value of exts later
        exts_new = exts.copy()

        # Insert user's input extension to exts_new in sorted order
        bisect.insort_left(exts_new, str(input_extension))
        # If input extension less than currently last extension
        if exts_last > input_extension:
            # Find input_extension index number in exts_new list
            input_extension_index = exts_new.index(str(input_extension))

            # Next sip positions after inserted
            next_positions = []

            # Iterate from input_extension index to exts last index
            for i in range(input_extension_index, len(exts)):
                # Add sip position to next_positions list
                next_positions.append(sips_data[exts[i]][1])

            # Add to next_positions list, convert back to string
            next_positions.append(str(exts_new_last_position))

            # Create list of new input data, including new position
            # Then add to sips_data
            input_data = [str(input_extension),
                          next_positions[0],
                          input_label,
                          input_context]

            sips_data[str(input_extension)] = input_data

            # Remove first index from next_positions
            next_positions.pop(0)

            n = 0  # set initial n value to 0

            # Iterate from after input_extension index to exts_new last index
            for i in range((input_extension_index + 1), len(exts_new)):
                # Update all sips position after
                sips_data[exts_new[i]][1] = next_positions[n]
                n += 1  # n = n + 1

        # Else if input extension greater than currently last extension
        else:
            # Create list of new input data, including new position
            # Then add to sips_data
            input_data = [str(input_extension),
                          exts_new_last_position,
                          input_label,
                          input_context]

            sips_data[str(input_extension)] = input_data

        # Write data to config file
        write_config(config, exts_new, sips_data)
        print('Extension number {0} succesfully added.'
              .format(str(input_extension)))

    # Delete extension
    elif sys.argv[1] == 'del':
        # Get sips data
        sips_data = sip_findall(config)

        if str(input_extension) in sips_data:
            # Display info and confirmation first before delete
            ext = sips_data[str(input_extension)][0]
            pos = sips_data[str(input_extension)][1]
            label = sips_data[str(input_extension)][2]
            context = sips_data[str(input_extension)][3]

            print('Ext. information: ')
            print('[SIP/{0}]'.format(ext))
            print('Position={0}'.format(pos))
            print('Label="{0}"'.format(label))
            print('Extension={0}'.format(ext))
            print('Context={0}'.format(context))
            print('icon=1\n')

            while True:
                confirm = input('Delete this extension?\n(y/n) ').strip()
                if confirm.lower() == 'y' or confirm.lower() == 'yes':
                    break
                elif confirm.lower() == 'n' or confirm.lower() == 'no':
                    print('Action cancelled. Exiting.')
                    sys.exit()
                else:
                    print('Please input only "y" or "n".')

            # Get sip position
            input_position = sips_data[str(input_extension)][1]

            # copy new exts list
            exts_new = exts.copy()
            # remove sip from new exts list
            exts_new.remove(str(input_extension))

            # remove last index in positions list
            positions.pop(len(exts_new))

            # Write data to config file
            del_config(exts_new, sips_data)
            print('Extension number {0} succesfully deleted.'
                  .format(str(input_extension)))
        else:
            print('That extension number does not exist. Exiting.')
            sys.exit()
    # View extension
    elif sys.argv[1] == 'view':
        # Find extension
        find_ext = sip_findone(config, input_extension)
        if find_ext:
            print(find_ext[0][0])
        else:
            print('That extension number does not exist. Exiting.')
            sys.exit()
    # Not a valid action
    else:
        print('Oops! That was not a valid actions. Exiting.')

# List all sips
elif len(sys.argv) == 2 and sys.argv[1] == 'list':
    # Get sips data
    sips_data = sip_findall(config)

    print('POS/EXT LABEL')
    # Iterate over all sips data
    for sip in sips_data:
        # Print the results to screen
        print('{0}/{1}'.format(sips_data[sip][1], sips_data[sip][2]))
# No arguments/parameters given, exiting
else:
    print('Please provide action or parameters. Exiting now.')
    sys.exit()
