#!/bin/bash

if [ $# -ne 5 ] ; then
  echo "Usage: $0 hosterUrl appId login password envName"
  exit 0
fi

. production/helpers.sh

HOSTER_URL=$1
APPID=$2
SESSION=$(getSession $3 $4 ${HOSTER_URL})
ENV_NAME=$5

stopEnv() {
  local session=$1
  local envName=$2
  echo "Stopping environment <$envName>..." >&2
  local cmd=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/stopenv -d "session=${session}&envName=${envName}")
  exitOnFail $cmd
  echo "Environment <$envName> stopped" >&2
  exit 0
}

stopEnv $SESSION $ENV_NAME
