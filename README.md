
# Projector HL Test

### Attacker
  Attacker is a docker container with py script. Does the actual slowloris attack.
  Opens 4096 sockets and sends headers with some delay not closing headers' sections.
  If some connections get closed by the server attacker will try reopen closed connections
  so that number of active connections is always about 4096.
  
  Build & start container from within attacker folder:
  * build:
  docker build -t slowloris .
  * run (specify victim's IP in .env file): docker-compose up
  
### Victim
  Victim is NGINX container. Will try to protect itself by applying the following:
  * default time out set now 15 s (not to serve never lasting slowloris requests)
  * set number of workers to 2 (increase default by 2) thus try increase number of workers to mitigate huge number of requests during the attack
  * set worker connections to 2048 (increase default by 2) same as above just allowing a worker to serve more connections
  * increase OS softlimit nofile option to 4096 for nginx(www-data) user to facilitate the above 
  
  Build & start container from within victim folder:
  * build docker build -t nginx .
  * run: docker-compose up
  
