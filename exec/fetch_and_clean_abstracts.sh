#!/bin/bash

echo 'Fetching PubMed abstracts based on the query:' "$QUERY"

python3 "$FETCH_ABSTRACTS" "$DATA_RAW" "$EMAIL" "$QUERY" "$QUERY"

echo 'Cleaning abstracts.'
python3 "$CLEAN_ABSTRACTS" "$DATA_RAW" "$DATA_PROC"

echo 'Done..'




