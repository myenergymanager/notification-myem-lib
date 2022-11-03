#!/bin/bash
cd tests/test_environment
export INTEGRATION_TESTS_NETWORK=${1:-docker_default}
export INTEGRATION_TESTS_CONTAINERS_PREFIX=${2:-local}
docker-compose -p $INTEGRATION_TESTS_CONTAINERS_PREFIX up -d
sleep 10

API_URL=http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${INTEGRATION_TESTS_CONTAINERS_PREFIX}_api_1):3000
export API_URL=$API_URL
API_KEY=$(python3 get_api_key.py)

cd ../..
echo "API_URL=${API_URL}" > dev_scripts/.local.env
echo "API_KEY=${API_KEY}" >> dev_scripts/.local.env
