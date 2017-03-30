NTP Client
run: main.py [-s server] [-v version] [-p port] [-d (debug)]
default:
	server: ntp.pool.org
	version: 2
	port: 123
	debug: false

---------------------

Deceiving SNTP server and client
run: sntp.py [-d delay] [-p port]
default:
	delay: 5 seconds
	port: 123

by Kirill Khapov