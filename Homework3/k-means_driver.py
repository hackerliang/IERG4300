import os
import logging

import numpy as np
import boto3
from botocore.exceptions import ClientError


def get_object(bucket_name, object_name):
    """Retrieve an object from an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: botocore.response.StreamingBody object. If error, return None.
    """

    # Retrieve the object
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket or object not found
        logging.error(e)
        return None
    # Return an open StreamingBody object
    return response['Body']


def generate_random_centroids():
    # Generate random centroids.
    random_centroids = np.random.randint(0, 255, size=(10, 784), dtype=int)
    # Save to txt
    with open('centroids/centroids_0.txt', 'w') as f:
        for idx in range(10):
            f.write('{}\t{}\n'.format(idx, str(random_centroids[idx].tolist())))
    # np.savetxt('centroids/centroids_0.txt', random_centroids.astype(int), fmt='%i', delimiter=',')


def run_mrjob(iteration_id):
    command = """
        hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -D mapred.map.tasks=10 \
        -D mapred.reduce.tasks=1 \
        -file centroids/centroids_{}.txt \
        -file k-means_mapper.py \
        -mapper "/usr/bin/python3 k-means_mapper.py" \
        -file k-means_reducer.py \
        -reducer "/usr/bin/python3 k-means_reducer.py" \
        -input s3://junru-big-data/mnist/train_images.txt \
        -output s3://junru-big-data/mnist/output/{}/ \
        -cmdenv "ITER_NUM={}"
    """.format(iteration_id - 1, iteration_id, iteration_id)
    logging.info('Executing command {}.'.format(command))
    os.system(command)


def get_new_centroids(iteration_id):
    # Assign these values before running the program
    bucket_name = 'junru-big-data'
    object_name = 'mnist/output/{}/part-00000'.format(iteration_id)
    # Retrieve the object
    stream = get_object(bucket_name, object_name)
    if stream is not None:
        # Read first chunk of the object's contents into memory as bytes
        new_result = stream.read().decode('utf8')
    # Save to file.
    with open('centroids/centroids_{}.txt'.format(iteration_id), 'w') as f:
        f.writelines(new_result)
    return new_result


def iteration(num_iterations):
    for i in range(1, num_iterations + 1):
        logging.info('Starting iteration {}.'.format(i))
        run_mrjob(i)
        get_new_centroids(i)
        logging.info('Finished iteration {}'.format(i))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    generate_random_centroids()
    iteration(10)
