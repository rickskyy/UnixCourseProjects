#!/bin/bash

#SOURCE_PATH=/home/rick/Projects
#DESTINATION_PATH=/home/rick/UnivProjects/UnixCourseProjects/lectures/lab1_task2/


SOURCE_PATH=$1
DESTINATION_PATH=$2


if [[ -z $SOURCE_PATH ]] ; then
    echo "Please enter source path"
    exit 1
elif [[ -z $DESTINATION_PATH ]] ; then 
    echo "Please enter destination path"
    exit 1
elif ! [ -d $SOURCE_PATH ] ; then
    echo "Invalid source path '$SOURCE_PATH'"
    exit 1
elif ! [ -d $DESTINATION_PATH ] ; then
    echo "Invalid destination path '$DESTINATION_PATH'"
    exit 1
elif [[ $SOURCE_PATH -ef $DESTINATION_PATH ]] ; then
    echo "Copying denied. Source path '$SOURCE_PATH' is equal to destination path '$DESTINATION_PATH'"
    exit 1
fi

read -p "Please enter file extension without a dot: " EXTENSION

echo "Searching files with $EXTENSION extension..."
FILES=$(find $SOURCE_PATH -type f -name '*.'$EXTENSION)

if [[ -z $FILES ]] ; then
    echo "No files with $EXTENSION found."
    exit 0 
fi
echo "Copying to $DESTINATION_PATH."

SIZE_BYTES=0
COUNT=0
while read -r FILE ; do
    CURRENT_SIZE=`wc -c $FILE | cut -d " " -f 1`
    SIZE_BYTES=$(($SIZE_BYTES + $CURRENT_SIZE))
    COUNT=$(($COUNT + 1))
done <<< "$FILES"

let "SIZE = $SIZE_BYTES / 1024"

mv $FILES $SOURCE_PATH/. $DESTINATION_PATH >> /dev/null

echo "Copied succesfully."
echo "Total files count: $COUNT"
echo "Total size: $SIZE KB"
