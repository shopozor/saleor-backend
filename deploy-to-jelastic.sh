#!/bin/bash

HOSTER_URL="https://app.hidora.com"
APPID="1dd8d191d38fff45e62564fcf67fdcd6"
CONTENT_TYPE="Content-Type: application/x-www-form-urlencoded; charset=UTF-8;";
USER_AGENT="Mozilla/4.73 [en] (X11; U; Linux 2.2.15 i686)"

startEnv() {
  local session=$1
  local envName=$2
  echo "Starting up environment <$envName>..." >&2
  curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/startenv -d "session=${session}&envName=${envName}"
  echo "Environment <$envName> started" >&2
}

startEnvIfNecessary() {
  local session=$1
  local envName=$2
  local envs=$3
  local envProps=$(echo $envs | jq '.infos[] | select(.env.envName=="${envName}")')
  local status=$(echo $envProps | jq '.env.status')
  if [ "$status" != "1" ] ; then
    startEnv $session "$envName"
  fi
}

getSession() {
  local login=$1
  local password=$2
  echo "Signing in..." >&2
  local signIn=$(curl -k -H "${CONTENT_TYPE}" -A "${USER_AGENT}"  -X POST \
    -fsS "${HOSTER_URL}/1.0/users/authentication/rest/signin" -d "login=$login&password=$password");
  echo 'Response signIn user: '$signIn >&2
  echo "Signed in" >&2
  echo $( jq '.session' <<< $signIn |  sed 's/\"//g' )
}

getEnvs() {
  local session=$1
  echo "Getting environments..." >&2
  local envs=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/getenvs -d "appid=${APPID}&session=${session}")
  echo "Got environments" >&2
  echo $envs
}

wasEnvCreated() {
  echo "envName = $2" >&2
  local envs=$1
  local envName=$2
  echo "Check if environment <$envName> exists..." >&2
  local envExists=$(echo $envs | jq '[.infos[].env.envName]' | jq "index(\"$envName\")")
  echo "Existence of environment <$envName> checked" >&2
  echo $envExists
}

installEnv() {
  local session=$1
  local envName=$2
  local pathToManifest=$3
  local manifest=$(cat $pathToManifest)
  echo "Installing new environment <$envName> from manifest <$pathToManifest>..." >&2
  local installApp=$(curl -k \
  -A "${USER_AGENT}" \
  -H "${CONTENT_TYPE}" \
  -X POST -fsS ${HOSTER_URL}"/1.0/development/scripting/rest/eval" \
  --data "session=${session}&shortdomain=${envName}&envName=${envName}&script=InstallApp&appid=appstore&type=install&charset=UTF-8" --data-urlencode "manifest=$manifest");
  echo "Environment <$envName> installed: "$installApp >&2
}

redeployEnvironment() {
  local session=$1
  local envName=$2
  local deployGroup=$3
  echo "Redeploying group <$deployGroup> of environment <$envName>" >&2
  curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/redeploycontainersbygroup \
    -d "appid=${APPID}&session=${session}&envName=${envName}&tag=latest&nodeGroup=${deployGroup}&useExistingVolumes=true&delay=20"
  echo "Environment redeployed" >&2
}

if [ $# -ne 3 ] ; then
  echo "Usage: $0 login password envName [deploy_group = cp] [path-to-manifest = manifest.jps]"
  exit 0
fi

ENV_NAME=$3
DEPLOY_GROUP=${4:-cp}
MANIFEST=${5:-manifest.jps}

SESSION=$(getSession $1 $2)
ENVS=$(getEnvs $SESSION)
CREATED=$(wasEnvCreated "$ENVS" "${ENV_NAME}")

# TODO: if the JPS manifest has changed, I need to re-install the environment, not only re-deploy

if [ "${CREATED}" == "null" ]; then
  installEnv $SESSION "${ENV_NAME}" "$MANIFEST"
else
  startEnvIfNecessary $SESSION "${ENV_NAME}" "$ENVS"
  redeployEnvironment $SESSION "${ENV_NAME}" ${DEPLOY_GROUP}
fi

exit 0
