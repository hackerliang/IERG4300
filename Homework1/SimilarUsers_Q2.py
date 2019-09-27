"""SimilarUsers.py
For Homework #1, IERG4300, S1 2019-2020, CUHK
Written by Junru Zhong (1155130306)
All rights reserved.

Last modified: Sept 28, 2019
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import csv


class UserPairsSameRates(MRJob):

    """This class is a MapReduce job.
    Extracts the user pairs rated same movie the same score.
    Output with the counts of the same rates on same movie.
    """

    # Enable secondary sort
    SORT_VALUES = True

    def mapper_movie_rating_user(self, _, line):
        """movieId be the key, the combination of rating and userId be the value."""
        # Convert each line into a dictionary
        row = dict(zip(['userId', 'movieId', 'rating'], [a.strip()
                                                         for a in csv.reader([line]).__next__()]))
        try:
            # Yield key-value pairs
            yield int(row['movieId']), (float(row['rating']), int(row['userId']))
        except ValueError:
            # Skip the first row.
            pass

    def reducer_extract_pairs_same_rates(self, _, values):
        """Extract the user pairs.
        Key: user pairs, values: 1 for same rating
        """
        users_same_rating = {}
        for item in values:
            if item[0] not in users_same_rating.keys():
                users_same_rating[item[0]] = [item[1]]
            else:
                users_same_rating[item[0]] += [item[1]]
        for _, users_list in users_same_rating.items():
            for i in range(0, len(users_list)):
                for j in range(i + 1, len(users_list)):
                    yield (users_list[i], users_list[j]), 1

    def mapper_sort_pairs(self, key, values):
        """Just pass the key-value pairs to sort them in key-order."""
        yield key, values

    def reducer_sum_pairs(self, key, values):
        """Sum up user pairs"""
        yield key, sum(values)

    def steps(self):
        """Defining steps to run multiple MapReduce jobs."""
        return [MRStep(mapper=self.mapper_movie_rating_user,
                       reducer=self.reducer_extract_pairs_same_rates),
                MRStep(mapper=self.mapper_sort_pairs,
                       reducer=self.reducer_sum_pairs)]


class UserPairsSameMovies(MRJob):

    """This class is a MapReduce job.
    Extracts the user pairs rated same movie (may NOT the same score).
    Output with the counts of the rated movie.
    """

    # Enable secondary sort
    SORT_VALUES = True

    def mapper_movie_rating_user(self, _, line):
        """movieId be the key, the combination of rating and userId be the value."""
        # Convert each line into a dictionary
        row = dict(zip(['userId', 'movieId', 'rating'], [a.strip()
                                                         for a in csv.reader([line]).__next__()]))
        try:
            # Yield key-value pairs
            # Will be sorted by movie_id (key), and rating (secondary sort)
            yield int(row['movieId']), (float(row['rating']), int(row['userId']))
        except ValueError:
            # Skip the first row.
            pass

    def reducer_extract_pairs_same_movie(self, _, values):
        """Extract the user pairs.
        Key: user pairs, values: 1
        """
        user_list = []
        # Append users to the list.
        for item in values:
            user_list.append(item[1])
        # Make the list into pairs.
        for i in range(0, len(user_list)):
            for j in range(i + 1, len(user_list)):
                # Yield and reverse key and value pair.
                yield (user_list[i], user_list[j]), 1

    def mapper_sort_pairs(self, key, values):
        """Just pass the key-value pairs to sort them in key-order."""
        yield key, values

    def reducer_sum_pairs(self, key, values):
        """Sum up user pairs"""
        yield key, sum(values)

    def steps(self):
        """Defining steps to run multiple MapReduce jobs."""
        return [MRStep(mapper=self.mapper_movie_rating_user,
                       reducer=self.reducer_extract_pairs_same_movie),
                MRStep(mapper=self.mapper_sort_pairs,
                       reducer=self.reducer_sum_pairs)]


class UserRatedMovies(MRJob):

    """This class is a MapReduce job.
    Extracts the total number of rates given by each user.
    """

    def mapper(self, _, line):
        """Extract users as keys."""
        # Convert each line into a dictionary
        row = dict(zip(['userId', 'movieId', 'rating'], [a.strip()
                                                         for a in csv.reader([line]).__next__()]))
        try:
            yield int(row['userId']), 1
        except ValueError:
            # Skip the first row.
            pass

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    # TODO: add configurations to save results to files.
    # UserRatedMovies.run()
    UserPairsSameRates.run()
