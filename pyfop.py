import re

sip_regex = re.compile(r'''(
    ((;?)\[SIP/(\d{2,4})\])\n   # 1: line, 2: commented, 3: ext. number
    (Position=(\d{1,3}))\n      # 4: line, 5: position
    (Label="(.*)")\n            # 6: line, 7: label
    (Extension=(\d{2,4}))\n     # 8: line, 9: ext. number
    (Context=(.*))\n            #10: line, 11: context
    (Icon=(\d+))\n              #12: line, 13: icon
    )''', re.IGNORECASE | re.VERBOSE)

config_file = open('./op_buttons.cfg')
config = config_file.read()
config_file.close()

result = sip_regex.findall(config)
print(len(result))
