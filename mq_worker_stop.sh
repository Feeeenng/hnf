# 停止
ps aux|grep celery_worker|awk '{print $2}'|xargs kill -9