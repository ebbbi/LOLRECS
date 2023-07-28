sed -i "s/{GITHUB_SHA}/$GITHUB_SHA/g" kubernetes/deployment.yaml
sed -i "s|{DB_URL}|$DB_URL|g" Dockerfile
