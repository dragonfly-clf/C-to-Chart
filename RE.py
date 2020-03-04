import re

Key = ['int', 'char', 'long long', 'long', 'void', 'unsigned int', 'unsigned long long', 'unsigned long', 'float', 'double', 'long double']

List = input()
for String in Key:
    x = String + r'\s+' + r'[a-zA-Z\_][0-9a-zA-Z\_]*' + r'[(.)]'
    if re.match(x, List):
        print(x)
        print(List)
