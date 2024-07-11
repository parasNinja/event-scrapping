sudo docker stop $(sudo docker ps -q --filter ancestor=event-backend)
sudo docker rm $(sudo docker ps -aq --filter ancestor=event-backend)
sudo docker build -f Dockerfile . -t event-backend:latest
sudo docker run -d --restart=always --network=host -v $(pwd)/:/app/ -v /tmp/:/tmp/ event-backend
