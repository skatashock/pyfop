import re

text = '''
djadlfdsfds
fsdfs
;START
ini dia 
ini doi
fdsfdf
ffsdfd
fdsfsdfsdf
sffssf
;END
dasddsdhkl
dadad
dda
'''

regex = re.compile(r';START([\s\S]+);END')
result = regex.search(text)
print(result.group())
