#!/bin/bash
### YYYY-M-D -> D.M.YYYY
READ_FROM_FILENAME=datetime_input.txt
OUTPUT_FILE=datetime_output.txt

regexp=$(<datetime_YYYY-M-D)
       
sed -E "s/$regexp/\1\7\8\9\.\4\5\.\2 /g" $READ_FROM_FILENAME > $OUTPUT_FILE

