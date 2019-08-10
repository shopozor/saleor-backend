#!/bin/bash

if [ $# -lt 5 ] ; then
  echo "Usage: $0 hosterUrl appId login password envName [deploy_group = cp] [path-to-manifest = manifest.jps] [tag = latest]"
  exit 0
fi

. production/helpers.sh

HOSTER_URL=$1
APPID=$2

SESSION=$(getSession $3 $4 ${HOSTER_URL})
ENV_NAME=$5
DEPLOY_GROUP=${6:-cp}
MANIFEST=${7:-manifest.jps}
TAG=${8:-latest}

wasEnvCreated() {
  echo "envName = $2" >&2
  local envs=$1
  local envName=$2
  echo "Check if environment <$envName> exists..." >&2
  local envExists=$(echo $envs | jq '[.infos[].env.envName]' | jq "index(\"$envName\")")
  echo "Existence of environment <$envName> checked" >&2
  echo $envExists
}

redeployEnvironment() {
  local session=$1
  local envName=$2
  local deployGroup=$3
  local tag=$4
  echo "Redeploying group <$deployGroup> of environment <$envName>" >&2
  local cmd=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/redeploycontainersbygroup \
    -d "appid=${APPID}&session=${session}&envName=${envName}&tag=${tag}&nodeGroup=${deployGroup}&useExistingVolumes=true&delay=20")
  # TODO: when the redeploy has worked, the exitOnFail interprets that as an error
  # exitOnFail $cmd
  echo "Environment redeployed" >&2
}

deployToJelastic() {
  ENVS=$(getEnvs $SESSION)
  CREATED=$(wasEnvCreated "$ENVS" "${ENV_NAME}")

  if [ "${CREATED}" == "null" ]; then
    installEnv $SESSION "${ENV_NAME}" "$MANIFEST"
    # the environment installed from the manifest deploys some tag that might not be the one we want
    # therefore, we redeploy with the desired tag
    redeployEnvironment $SESSION "${ENV_NAME}" ${DEPLOY_GROUP} ${TAG}
  else
    startEnvIfNecessary $SESSION "${ENV_NAME}" "$ENVS"
    redeployEnvironment $SESSION "${ENV_NAME}" ${DEPLOY_GROUP} ${TAG}
  fi

  # TODO: restart container!

  exit 0
}

deployToJelastic
