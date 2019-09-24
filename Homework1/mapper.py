#!usr/bin/python3
"""mapper.py
For each of the incoming record, re-organize as the 'key-value' form.
Key: (movie_id, rating), value: user_id
"""

import fileinput

# Remove the first line.
lines = fileinput.input()
next(lines)

for line in lines:
    # Remove white spaces and line feed.
    line = line.strip()
    # Split each line into a list of information.
    line_data = line.split(',', 2)
    # Reorganize the data and output.
    print('({}, {})\t{}'.format(line_data[1], line_data[2], line_data[0]))
