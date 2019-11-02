hadoop jar /usr/hdp/2.4.2.0-258/hadoop-mapreduce/hadoop-streaming.jar \
-D mapred.map.tasks=10 \
-D mapred.reduce.tasks=1 \
-file son_step_1_mapper.py \
-mapper "/usr/bin/python3 son_step_1_mapper.py" \
-file son_step_1_reducer.py \
-reducer "/usr/bin/python3 son_step_1_reducer.py" \
-input shakespeare_basket/ \
-output hw2_son_step_1_output/
