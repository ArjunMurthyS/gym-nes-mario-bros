# Makefile to send this to Zam
SHELL=/usr/bin/env /bin/bash

# Senders:
send:	send_zamok
send_zamok:
	CP --exclude=.git ./ ${Szam}me/

send_ws3:
	CP --exclude=.git ./ lilian_besson@ws3:~/nesgym.git/