#!/bin/bash

cd tests/test_environment
export INTEGRATION_TESTS_NETWORK=${1:-docker_default}
export INTEGRATION_TESTS_CONTAINERS_PREFIX=${2:-local}
docker-compose -p $INTEGRATION_TESTS_CONTAINERS_PREFIX down -v

cd ..
