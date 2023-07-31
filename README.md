celery -A eportal worker -l info -P eventlet

docker ps -a | grep "web" | awk '{print $1}' | xargs docker start

