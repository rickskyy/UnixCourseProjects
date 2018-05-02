#!/bin/bash

READ_FROM_FILENAME=utf_text.txt
OUTPUT_FILE=utf_output.txt

utf_regexp=$(<utf-16_regex)

found_characters=$(grep -E -o "$utf_regexp" "$READ_FROM_FILENAME")

if [ -n "$found_characters" ]; then
    echo $found_characters > $OUTPUT_FILE
else
    echo "Nothing found. No output required"
fi
