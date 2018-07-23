#!/bin/bash

# We want to resize any images larger than 224x300 down to 
# 224x300, but keep the aspect ratio in the process. Now because
# we are enforcing aspect ratio correctness, we may not get
# the exact size image we want. So have a canvas of size 224x300
# and put the resulting resized image centered on that.

if [[ ! -v DEEPFASHION_FOLDER ]]; then
  echo "Error: set DEEPFASHION_FOLDER variable in env.sh, and source the file"
  exit 1
fi

cd $DEEPFASHION_FOLDER/Img
mkdir img_converted
for foldername in `ls img`; do
  for file in `ls img/$foldername/*.jpg`; do
    infile=$file
    outfolder=img_converted/$foldername
    if [ ! -d $outfolder ]; then
      mkdir $outfolder
    fi
    outfile=$outfolder/`basename $file`
    convert $infile -resize 224x300\> -background "rgb(255,255,255)" -gravity center -extent 224x300 $outfile
    echo $infile "-->" $outfile
  done
done
