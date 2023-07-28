docker build -t backend-image .

docker run -d --name backend -p 80:80 backend-image
