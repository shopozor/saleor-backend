CONTENT_TYPE="Content-Type: application/x-www-form-urlencoded; charset=UTF-8;"
USER_AGENT="Mozilla/4.73 [en] (X11; U; Linux 2.2.15 i686)"

getCommandResult() {
  local command=$1
  echo $(echo $command | jq '.result')
}

exitOnFail() {
  local command=$1
  local result=$(getCommandResult $command)
  if [[ "$result" != "0" ]] ; then
    echo "Following command failed with result $result: $command" >&2
    exit 1
  fi
}

getSession() {
  local login=$1
  local password=$2
  local hosterUrl=$3
  echo "Signing in..." >&2
  local cmd=$(curl -k -H "${CONTENT_TYPE}" -A "${USER_AGENT}"  -X POST \
    -fsS "$hosterUrl/1.0/users/authentication/rest/signin" -d "login=$login&password=$password");
  exitOnFail $cmd
  echo "Signed in" >&2
  echo $(jq '.session' <<< $cmd |  sed 's/\"//g')
}

getEnvs() {
  local session=$1
  echo "Getting environments..." >&2
  local cmd=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/getenvs -d "appid=${APPID}&session=${session}")
#  exitOnFail $cmd
  echo "Got environments" >&2
  echo $cmd
}

startEnv() {
  local session=$1
  local envName=$2
  echo "Starting up environment <$envName>..." >&2
  local cmd=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/startenv -d "session=${session}&envName=${envName}")
  exitOnFail $cmd
  echo "Environment <$envName> started" >&2
}

startEnvIfNecessary() {
  local session=$1
  local envName=$2
  local envs=$3
  local status=$(echo $envs | jq ".infos[] | select(.env.envName==\"$envName\") | .env.status")
  if [ "$status" != "1" ] ; then
    startEnv $session "$envName"
  fi
}

waitUntilEnvIsRunning () {
  local session=$1
  local envName=$2
  while true
  do
    local envInfo=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/getenvinfo -d "session=${session}&envName=${envName}")
    STATUS=$(echo $envInfo | jq '.env.status')
    if [ "$STATUS" == "1" ] ; then
      break;
    else
      sleep 1
    fi
  done
}

installEnv() {
  local session=$1
  local envName=$2
  local pathToManifest=$3
  local manifest=$(cat $pathToManifest)
  echo "Installing new environment <$envName> from manifest <$pathToManifest>..." >&2
  local cmd=$(curl -k \
    -A "${USER_AGENT}" \
    -H "${CONTENT_TYPE}" \
    -X POST -fsS ${HOSTER_URL}"/1.0/development/scripting/rest/eval" \
    --data "session=${session}&shortdomain=${envName}&envName=${envName}&script=InstallApp&appid=appstore&type=install&charset=UTF-8" --data-urlencode "manifest=$manifest")
  echo "Installation result: $cmd" >&2
  # From our experience, Jelastic is not reliable enough to assume that the previous command was really
  # successful upon return. Therefore we check that the environment is really running after that command.
  waitUntilEnvIsRunning $session $envName
  echo "Environment <$envName> installed" >&2
}