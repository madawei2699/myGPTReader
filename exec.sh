docker build -t robot-quick-start .
docker run --env-file .env -p 3000:3000 -it robot-quick-start
