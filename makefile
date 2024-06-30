run:
	nohup gunicorn -w 4 -b 0.0.0.0:443 app:app --certfile=www.policy-scut.cn_public.crt --keyfile=www.policy-scut.cn.key &
kill:
	pkill -f app