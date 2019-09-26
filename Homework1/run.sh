#!/bin/bash
/home/junru/Apps/hadoop-2.9.2/bin/hadoop jar \
    /home/junru/Apps/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -file mapper.py \
    -mapper "/usr/bin/python3 mapper.py" \
    -file reducer.py \
    -reducer "/usr/bin/python3 reducer.py" \
    -input input/ \
    -output intermediate/

/home/junru/Apps/hadoop-2.9.2/bin/hadoop jar \
    /home/junru/Apps/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
    -file mapper2.py \
    -mapper "/usr/bin/python3 mapper2.py" \
    -file reducer2.py \
    -reducer "/usr/bin/python3 reducer2.py" \
    -input intermediate/part-00000 \
    -output output/