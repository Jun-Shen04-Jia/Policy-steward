run:
	nohup gunicorn -w 4 -b 0.0.0.0:443 app:app --certfile=../ssl/www.policy-scut.cn_public.crt --keyfile=../ssl/www.policy-scut.cn.key > ../app.log 2>&1 &
kill:
	pkill -f app
	rm -f ../app.log