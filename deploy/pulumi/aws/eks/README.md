kubectl create secret docker-registry regcred \
  --docker-server=491489166083.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password) \
  --namespace=alanc-crapi