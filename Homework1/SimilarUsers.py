from mrjob.job import MRJob
from mrjob.step import MRStep
import csv

class SimilarUsers(MRJob):

    # Enable secondary sort
    SORT_VALUES = True

    def step_1_mapper(self, _, line):
        """movieId be the key, the combination of rating and userId be the value."""
        # Convert each line into a dictionary
        row = dict(zip(['userId', 'movieId', 'rating'], [a.strip() for a in csv.reader([line]).__next__()]))
        try:
            # Yield key-value pairs
            # Will be sorted by movie_id (key), and rating (secondary sort)
            yield int(row['movieId']), (float(row['rating']), int(row['userId']))
        except ValueError:
            # Skip the first row.
            pass

    def step_1_reducer(self, movie_id, values):
        """Find the users that give one movie the same rating."""
        users_same_rating = {}
        for item in values:
            if item[0] not in users_same_rating.keys():
                users_same_rating[item[0]] = [item[1]]
            else:
                users_same_rating[item[0]] += [item[1]]
        yield movie_id, users_same_rating

    def step_2_mapper(self, movie_id, users_same_rating):
        """Extract the user pairs from users that gave one movie the same rating."""
        for rating, users_list in users_same_rating.items():
            for i in range(0, len(users_list)):
                for j in range(i + 1, len(users_list)):
                    yield (users_list[i], users_list[j]), 1
    
    def step_2_reducer(self, user_pair, counts):
        """Sum up the total counts for same ratings."""
        yield None, (sum(counts), user_pair)

    def step_3_reducer(self, _, total_counts):
        # Modify `reverse` parameter for sorting order.
        # reverse=True: descending order,
        # reverse=False: ascending order.
        for count, key in sorted(total_counts, reverse=False):
            yield int(count), key

    def steps(self):
        return [MRStep(mapper=self.step_1_mapper,
                       reducer=self.step_1_reducer),
                MRStep(mapper=self.step_2_mapper,
                       reducer=self.step_2_reducer),
                MRStep(reducer=self.step_3_reducer)]

if __name__ == '__main__':
    SimilarUsers.run()