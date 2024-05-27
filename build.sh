tox
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg VERSION=$(git describe) \
  --push -t 936272581790.dkr.ecr.us-west-1.amazonaws.com/cumulonimbusinfrastructurestackecrb011c8ff-localcloudagent882a885f-uf9f1uyibbfx .

docker pull 936272581790.dkr.ecr.us-west-1.amazonaws.com/cumulonimbusinfrastructurestackecrb011c8ff-pythona57b7ce0-zwlwp6r36elt
