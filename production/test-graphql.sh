#! /bin/bash

if [ $# -ne 1 ] ; then
    echo "Usage: $0 <graphql-endpoint-url>"
    exit 1
fi

GRAPHQL_URL=$1

EXPECTED_RESPONSE='{"errors": [{"message": "You do not have permission to perform this action", "locations": [{"line": 1, "column": 9}], "path": ["me"]}], "data": {"me": null}}'

# TODO: 1. curl during 5 minutes until it does not return 502
while [[ $status -ne 200 ]] ; do
    cmd=$(curl -H "Content-Type: application/json" \
        -w "#%{http_code}" \
        -d '{ "query": "query { me { id } }", "variables": "{}" }' \
        -s \
        -X POST \
        $GRAPHQL_URL)
    status=$(echo $cmd | cut -d '#' -f 2)
done

body=$(echo $cmd | cut -d '#' -f 1)
[ "$EXPECTED_RESPONSE" == "$body" ] && exit 0 || exit 1