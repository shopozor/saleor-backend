#!/bin/bash

if [ $# -ne 3 ] ; then
  echo "Usage: $0 login password envName [deploy_group = cp]"
  exit 0
fi

HOSTER_URL="https://app.hidora.com"
ENV_NAME=$3
APPID="1dd8d191d38fff45e62564fcf67fdcd6"
CONTENT_TYPE="Content-Type: application/x-www-form-urlencoded; charset=UTF-8;";
USER_AGENT="Mozilla/4.73 [en] (X11; U; Linux 2.2.15 i686)"
DEPLOY_GROUP=${4:-cp}

echo "SignIn...";
signIn=$(curl -k -H "${CONTENT_TYPE}" -A "${USER_AGENT}"  -X POST \
-fsS "${HOSTER_URL}/1.0/users/authentication/rest/signin" -d "login=$1&password=$2");
echo 'Response signIn user: '$signIn

echo "SignIn...2";

SESSION=$( jq '.session' <<< $signIn |  sed 's/\"//g' );

echo "Check if env is created...";
envs=$(curl -k \
-H "${CONTENT_TYPE}" \
-A "${USER_AGENT}" \
-X POST \
-fsS ${HOSTER_URL}/1.0/environment/control/rest/getenvs -d "appid=${APPID}&session=${SESSION}");
echo "Envs = $envs"
ENVNAMES=$(echo $envs | jq '[.infos[].env.envName]')
CREATED=$(echo $envs | jq '[.infos[].env.envName]' | jq "index(\"$ENV_NAME\")")

# TODO: need to check whether the environment is up and running in order to deploy???
if [[ "${CREATED}" == "null" ]]; then
  echo "Install new environment...";
  #MANIFEST=$(cat manifest.jps)
  #installApp=$(curl -k \
  #-A "${USER_AGENT}" \
  #-H "${CONTENT_TYPE}" \
  #-X POST -fsS ${HOSTER_URL}"/1.0/development/scripting/rest/eval" \
  #--data "session=${SESSION}&shortdomain=${ENV_NAME}&envName=${ENV_NAME}&script=InstallApp&appid=appstore&type=install&charset=UTF-8" --data-urlencode "manifest=$MANIFEST");
  #echo "Response install env: "$installApp;
else
  echo "Redeploy existing environment (Group ${DEPLOY_GROUP})..."
  #redeploy=$(curl -k \
  #-H "${CONTENT_TYPE}" \
  #-A "${USER_AGENT}" \
  #-X POST \
  #-fsS ${HOSTER_URL}/1.0/environment/control/rest/redeploycontainersbygroup \
  #-d "appid=${APPID}&session=${SESSION}&envName=${ENV_NAME}&tag=latest&nodeGroup=${DEPLOY_GROUP}&useExistingVolumes=true&delay=20");
  #echo "Environment redeployed"
fi

exit 0
