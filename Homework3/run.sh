#!/usr/bin/env bash

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-D mapred.map.tasks=10 \
-D mapred.reduce.tasks=1 \
-file s3://YOUR BUCKET/mnist/centroids.txt \
-file k-means_mapper.py \
-mapper "/usr/bin/python3 k-means_mapper.py" \
-file k-means_reducer.py \
-reducer "/usr/bin/python3 k-means_reducer.py" \
-input s3://YOUR BUCKET/mnist/train_images.txt \
-output s3://YOUR BUCKET/mnist/output/