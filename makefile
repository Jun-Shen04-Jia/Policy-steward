run:
	nohup gunicorn -w 4 -b 0.0.0.0:443 app:app --certfile=../ssl/www.policy-scut.cn_public.crt --keyfile=../ssl/www.policy-scut.cn.key > ../app_https.log 2>&1 &
	nohup gunicorn -w 4 -b 0.0.0.0:80 app:app > ../app_http.log 2>&1 &
kill:
	pkill -f app
	rm -f ../app*.log