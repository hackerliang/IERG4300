#!usr/bin/python3
"""mapper.py
For each of the incoming record, re-organize as the 'key-value' form.
Key: (movie_id, user_id), value: rating
"""

import sys
import fileinput

# Remove the first line.
lines = sys.stdin
next(lines)

for line in lines:
    # Remove white spaces and line feed.
    line = line.strip()
    # Split each line into a list of information.
    line_data = line.split(',', 2)
    # Reorganize the data and output.
    sys.stdout.write('(%s, %s)\t%s'.format(line_data[1], line_data[0], line_data[2]))
