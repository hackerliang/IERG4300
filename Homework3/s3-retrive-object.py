import logging
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


def main():
    """Exercise get_object()"""

    # Assign these values before running the program
    test_bucket_name = 'YOUR BUCKET NAME'
    test_object_name = 'mnist/output/1/part-00000'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Retrieve the object
    stream = get_object(test_bucket_name, test_object_name)
    if stream is not None:
        # Read first chunk of the object's contents into memory as bytes
        data = stream.read()

        # Output object's beginning characters
        logging.info(f'{test_object_name}: {data[:60]}...')


if __name__ == '__main__':
    main()