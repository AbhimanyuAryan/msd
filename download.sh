#!/bin/bash

curl -L -o images.txt https://bit.ly/2JcmBIU
curl -L -o crops.txt https://bit.ly/2DYz9iw

mkdir images && mkdir crops

file1="images.txt"
file2="crops.txt"

# download images parallely 
#while IFS=$'\t' read -r f1 f2
#do
 # printf 'f1: %s\n' "$f1"
 # printf 'f2: %s\n' "$f2"
 # cd images && { curl -O -J $f1 ;cd -; }
 # cd crops && { curl -O -J $f2 ;cd -; } 
#done < <(paste $file1 $file2)

while read p; do
  #echo "$p"
  cd images && { curl -O -J -L "$p" ;cd -; }
done <images.txt

while read p; do
  #echo "$p"
  cd crops && { curl -O -J -L "$p" ;cd -; }
done <crops.txt