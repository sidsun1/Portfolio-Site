#!/bin/bash

NEW_IDS=()
NUM_REQ=$(( RANDOM % 11 + 10 ))

for ((i=1; i<=NUM_REQ; i++)); do
	REQ=$(curl -s -X POST http://localhost:5000/api/timeline_post -d "name=$RANDOM" -d "email=email@$RANDOMdomain" -d "content=Testing at $(date) POST req w/ curl")
	echo "$REQ"
	NEW_ID=$(echo "$REQ" | jq -r '.timeline_posts[-1].id')
	echo "Sent over POST req $i of $NUM_REQ"
	
	VAL=$(curl -s -X GET http://localhost:5000/api/timeline_post/$NEW_ID)
	if [ -n "$VAL" ]; then
		echo "Received POST req $NEW_ID of $NUM_REQ"
	fi
	NEW_IDS+=($NEW_ID)
done


for ID in "${NEW_IDS[@]}"; do
   curl -s -X DELETE http://localhost:5000/api/timeline_post/$ID
   echo "Deleted POST ID: $ID"
done
