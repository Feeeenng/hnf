# 启动, ps：1.-c是并发数, -c1是阻塞队列;2.--autoreload 自动加载修改, 该选项在4.0版本后被删除
nohup python mq\celery_worker.py worker --autoreload -c2 -n common_worker -Q common -l info > /data/log/celery_common_worker.log &
nohup python mq\celery_worker.py worker --autoreload -c2 -n email_worker -Q email -l info > /data/log/celery_email_worker.log &
nohup python mq\celery_worker.py worker --autoreload -c2 -n file_worker -Q file -l info > /data/log/celery_file_worker.log &