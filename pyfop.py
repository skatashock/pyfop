import sys
import re
import bisect

# Example data:
# [Sip/2003]
# Position=17
# Label="2003 B.S"
# Extension=2003
# Context=internal-mas
# icon=1

input_extension = input('Extension number: ').strip()
input_label = input('Label: ').strip()
input_context = input('Context: ').strip()

sip_regex = re.compile(r'''(
    ((;?)\[SIP/(\d{2,4})\])\n   # 1: line, 2: commented, 3: ext. number
    (Position=(\d{1,3}))\n      # 4: line, 5: position
    (Label="(.*)")\n            # 6: line, 7: label
    (Extension=(\d{2,4}))\n     # 8: line, 9: ext. number
    (Context=(.*))\n            # 10: line, 11: context
    (Icon=(\d+))\n              # 12: line, 13: icon
    )''', re.IGNORECASE | re.VERBOSE)

config_file = open('./op_buttons.cfg')
config = config_file.read()
config_file.close()

results = sip_regex.findall(config)
exts = []
sips_data = {}

for result in results:
    extension = result[3]
    position = result[5]
    label = result[7]
    context = result[11]

    exts.append(extension)

    extension_data = [extension, position, label, context]
    sips_data[extension] = extension_data

bisect.insort_left(exts, input_extension)

input_data = [input_extension, '9999', input_label, input_context]
sips_data[input_extension] = input_data

for ext in exts:
    print('[SIP/{0}]\n'.format(sips_data[ext][0]))
