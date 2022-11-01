#!/bin/bash
cd tests/test_environment
export INTEGRATION_TESTS_NETWORK=${1:-docker_default}
export PREFIX=${2:-local}
docker-compose -p $PREFIX up -d
sleep 10

API_URL=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${PREFIX}_api_1)
API_KEY=$(python3 -c 'import get_api_key; get_api_key.main('\"$API_URL\"')')

cd ../..
echo "API_URL=http://${API_URL}:3000" > dev_scripts/.local.env
echo "API_KEY=${API_KEY}" >> dev_scripts/.local.env
