#!/usr/bin/env python3

nice_names = {}
with open("docs/nice_names.txt") as f:
    for line_num, line in enumerate(f):
        for nice_name in line.split():
            nice_names[nice_name] = line_num

with open('lib/nicenames.py', 'w') as f:
    f.write("#!/usr/bin/env python3\n")
    f.write("nice_names = " + repr(nice_names) + "\n")