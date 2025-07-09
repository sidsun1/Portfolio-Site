#!/bin/bash

LAST_ID_BEFORE=$(curl -s -X GET http://localhost:5000/api/timeline_post | jq '[.timeline_posts[].id] | max // 0')
NEW_IDS=()
NUM_REQ=$(( RANDOM % 11 + 10 ))

for ((i=1; i<=NUM_REQ; i++)); do
	REQ=$(curl -s -X POST http://localhost:5000/api/timeline_post -d "name=$RANDOM" -d "email=email@$RANDOM.domain" -d "content=Testing at $(date) POST req w/ curl")
	echo "$REQ"
	NEW_ID=$(echo "$REQ" | jq -r '.id')
	echo "Sent over POST req $i of $NUM_REQ"

	VAL=$(curl -s -X GET http://localhost:5000/api/timeline_post/$NEW_ID)
	if [ -n "$VAL" ]; then
		echo "Received POST req $NEW_ID"
	fi
	NEW_IDS+=($NEW_ID)
done


for ID in "${NEW_IDS[@]}"; do
    if [ "$ID" -gt "$LAST_ID_BEFORE" ]; then
        curl -s -X DELETE http://localhost:5000/api/timeline_post/$ID
        echo "Deleted POST ID: $ID"
    else
        echo "Skipped pre-existing POST ID: $ID"
    fi
done