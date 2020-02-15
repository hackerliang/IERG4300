"""SimilarUsers.py
For Homework #1, IERG4300, S1 2019-2020, CUHK
Written by Junru Zhong
All rights reserved.

Last modified: Sept 28, 2019
"""

import csv
import json
from operator import itemgetter

from mrjob.job import MRJob
from mrjob.step import MRStep


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


def calculate_similarity():
    """This is a sequential job.
    Reads the intermediate files generated by previous jobs, match and calculate the similarity score.
    """

    # Read user rated movies to a dictionary.
    user_rated_movies = {}
    for row in csv.reader(open('q2_user_rated_movies.txt'), delimiter='\t'):
        user_rated_movies[int(row[0])] = int(row[1])
    # Read user pairs have same rates to dictionary.
    user_pairs_same_rate = {}
    for row in csv.reader(open('q2_user_pairs_same_rate.txt'), delimiter='\t'):
        # Convert the user ids into integer tuples.
        user_ids = row[0][1:-1].split(',')
        user_pairs_same_rate[(int(user_ids[0]), int(user_ids[1]))] = int(row[1])
    # Read user pairs have rated same movies to dictionary.
    user_pairs_same_movie = {}
    for row in csv.reader(open('q2_user_pairs_same_movie.txt'), delimiter='\t'):
        user_ids = row[0][1:-1].split(',')
        user_pairs_same_movie[(int(user_ids[0]), int(user_ids[1]))] = int(row[1])

    """Calculate similarity scores.
    For all user pairs that have rated same movie a same score,
      1. find the numbers of rated movies for EACH user.
      2. find the numbers of rated movies for BOTH users.
      3. calculates the similarity scores.
      4. save the score to a dictionary with the first user id as the keys.
    The output dictionary will be:
      {user-id: [[user-id, score], [user-id, score], ...]}
    Sort each value of the output dictionary by the score, in decending order.
    """
    
    scores = {}
    for user_pair, number_same_rate in user_pairs_same_rate.items():
        # Number of rated movies for EACH user.
        number_rated_movie_0 = user_rated_movies[user_pair[0]]
        number_rated_movie_1 = user_rated_movies[user_pair[1]]
        # Number of rated movies for BOTH users.
        number_both_rated = user_pairs_same_movie[user_pair]
        # Calculate the score.
        try:
            score = number_same_rate / (number_rated_movie_0 + number_rated_movie_1 - number_both_rated)
        except ZeroDivisionError:
            score = 0
        # Add the score to the dictionary.
        if user_pair[0] not in scores.keys():
            scores[user_pair[0]] = [[user_pair[1], score]]
        else:
            scores[user_pair[0]] += [[user_pair[1], score]]
    # Sort by scores for each value in scores dictionary.
    for key, value in scores.items():
        scores[key] = sorted(value, key=itemgetter(1), reverse=True)
    
    # Output the dictionary to a json file.
    json.dump(scores, open('scores.json', 'w'), indent=2)

    # Filter scores by my student ID, and top-3 similar users, dumps to the json file too.
    filtered_scores = {}
    for key, value in scores.items():
        if str(key).endswith('06'):
            filtered_scores[key] = value[:3]
    json.dump(filtered_scores, open('filtered_scores.json', 'w'), indent=2)

if __name__ == '__main__':
    # FIRST: run these three MR tasks.
    # UserRatedMovies.run()
    # UserPairsSameRates.run()
    UserPairsSameMovies.run()

    # THEN: calaculate similarity scores by this function.
    # calculate_similarity()
