from SimilarUsers_Q1 import SimilarUsers
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)-15s %(levelname)-8s %(message)s'
)
log = logging.getLogger('submitjobs')

def main():
    cluster_id = 'ierg4300'
    # log.info('Cluster: {}'.format(cluster_id))
    mr_job = SimilarUsers(
        args=[
            '-r', 'dataproc',
            '--output-dir', 'gs://dataproc-data-storage/movie-rating-output',
            '--cluster-id', cluster_id,
            # 'gs://dataproc-data-storage/movie-rating-input/large_dataset.csv'
            # '-D mapred.reduce.tasks=1000'
        ]
    )
    runner = mr_job.make_runner()
    # runner.input_paths=['gs://dataproc-data-storage/movie-rating-input/large_dataset.csv']
    runner._launch()

if __name__ == '__main__':
    main()