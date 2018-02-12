# 启动
nohup python mq\celery_worker.py worker -c2 -n common_worker -Q common -l info > /data/log/celery_common_worker.log &
nohup python mq\celery_worker.py worker -c2 -n email_worker -Q email -l info > /data/log/celery_email_worker.log &
nohup python mq\celery_worker.py worker -c2 -n file_worker -Q file -l info > /data/log/celery_file_worker.log &

# 停止
ps aux|grep celery_worker|awk '{print $2}'|xargs kill -9