#! /bin/bash

if [ $# -ne 1 ] ; then
  echo "Usage: $0 <path-to-root-repo>"
  echo "Example: $0 /home/user/workspace/shopozor-backend"
  exit 1
fi

ROOT=$1

cd $ROOT
pre-commit install
cd $ROOT/features/graphql
pre-commit install
cd $ROOT/features/fixtures
pre-commit install
