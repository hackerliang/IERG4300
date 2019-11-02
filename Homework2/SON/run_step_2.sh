hadoop jar /usr/hdp/2.4.2.0-258/hadoop-mapreduce/hadoop-streaming.jar \
-D mapred.map.tasks=10 \
-D mapred.reduce.tasks=1 \
-file step_1_result.txt \
-file son_step_2_mapper.py \
-mapper "/usr/bin/python3 son_step_2_mapper.py" \
-file son_step_2_reducer.py \
-reducer "/usr/bin/python3 son_step_2_reducer.py" \
-input shakespeare_basket/ \
-output hw2_son_step_2_output/
