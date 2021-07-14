source /home/biomind/.profile
pm2 delete triton
pm2 delete annotation
pm2 delete predictor
sleep 5
kill -9 $(ps -ef | grep manage.py | awk '{print $2}')
ps -ef | grep manage.py