#!/bin/bash

SEARCH_PATH=$1

if [[ -z $SEARCH_PATH ]] ; then
    echo "Please enter search path"
    exit 1
elif ! [ -d $SEARCH_PATH ] ; then
    echo "Invalid search path '$SEARCH_PATH'"
    exit 1
else
    echo "Listing directories from $SEARCH_PATH..."
fi

SUB_DIRS=$(find $SEARCH_PATH -type d)

countSubDirs() {
	for DIR in $SUB_DIRS
	do
		NFILES=$(find $DIR -maxdepth 1 | wc -l)
		printf "%d %s\n" $NFILES "$DIR" 
	done
}

CATALOG=$(countSubDirs | sort -nr)

read -p "Please enter destination filename: " DESTINATION
echo "$CATALOG">"$DESTINATION"

