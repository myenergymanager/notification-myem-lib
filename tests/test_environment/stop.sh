#!/bin/bash

cd tests/test_environment
export INTEGRATION_TESTS_NETWORK=${1:-docker_default}
export PREFIX=${2:-local}
docker-compose -p $PREFIX down -v

cd ..
