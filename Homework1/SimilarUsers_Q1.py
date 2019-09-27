"""SimilarUsers.py
For Homework #1, IERG4300, S1 2019-2020, CUHK
Written by Junru Zhong (1155130306)
All rights reserved.

Last modified: Sept 26, 2019
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import csv


class SimilarUsers(MRJob):

    # Enable secondary sort
    SORT_VALUES = True

    def step_1_mapper(self, _, line):
        """movieId be the key, the combination of rating and userId be the value."""
        # Convert each line into a dictionary
        row = dict(zip(['userId', 'movieId', 'rating'], [a.strip()
                                                         for a in csv.reader([line]).__next__()]))
        try:
            # Yield key-value pairs
            # Will be sorted by movie_id, and rating (key)
            yield (int(row['movieId']), float(row['rating'])), int(row['userId'])
        except ValueError:
            # Skip the first row.
            pass

    def step_1_reducer(self, key, values):
        user_list = []
        # Append users to the list with same rating for a movie.
        for item in values:
            user_list.append(item)
        # Make the list into pairs.
        for i in range(0, len(user_list)):
            for j in range(i + 1, len(user_list)):
                # Yield and reverse key and value pair.
                yield (user_list[i], user_list[j]), 1
    
    def step_2_reducer(self, key, values):
        """Sum up the values."""
        yield None, (sum(values), key)

    def step_3_reducer(self, _, values):
        """Sort the values."""
        for count, key in sorted(values, reverse=True):
            yield int(count), key

    def steps(self):
        """Defining steps to run multiple MapReduce jobs."""
        return [MRStep(mapper=self.step_1_mapper,
                       reducer=self.step_1_reducer),
                MRStep(reducer=self.step_2_reducer),
                MRStep(reducer=self.step_3_reducer)]


if __name__ == '__main__':
    SimilarUsers.run()
