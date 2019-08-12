#! /bin/bash

if [ $# -ne 1 ] ; then
    echo "Usage: $0 <graphql-endpoint-url>"
    exit 1
fi

GRAPHQL_URL=$1

EXPECTED_RESPONSE='{"errors": [{"message": "You do not have permission to perform this action", "locations": [{"line": 1, "column": 9}], "path": ["me"]}], "data": {"me": null}}'

TIME_OUT_IN_SECONDS=300
TIMER_DELTA_IN_SECONDS=5
START_TIME=`date +%s`
while [[ $status -ne 200 ]] ; do
    status=$(curl -H "Content-Type: application/json" \
        -w "%{http_code}" \
        -d '{ "query": "query { me { id } }", "variables": "{}" }' \
        -so /dev/null \
        -X POST \
        $GRAPHQL_URL)
    CURRENT_TIME=`date +%s`
    RUNTIME=$((CURRENT_TIME - START_TIME))
    [ $RUNTIME -ge $TIME_OUT_IN_SECONDS ] && exit 1
    sleep $TIMER_DELTA_IN_SECONDS
done

body=$(curl -H "Content-Type: application/json" \
    -d '{ "query": "query { me { id } }", "variables": "{}" }' \
    -s \
    -X POST \
    $GRAPHQL_URL)

[ "$EXPECTED_RESPONSE" == "$body" ] && exit 0 || exit 1