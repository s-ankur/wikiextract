#!/bin/bash

set -e
set -x

if [ ! -f hiwiki-pages-meta-current.xml ]; then
echo "DOWNLOADING HIWIKI"
# You may need to update this link as older dumps are deleted all the time. Point it to a "current" wiki dump
curl -L --fail  --remote-name-all https://dumps.wikimedia.org/hiwiki/20200601/hiwiki-20200601-pages-meta-current.xml.bz2   --output hiwiki-pages-meta-current.xml.bz2
bzip2 -d  hiwiki-pages-meta-current.xml.bz2
rm hiwiki-pages-meta-current.xml.bz2
fi


if [ ! -d hindi-pos-tagger-3.0 ]; then
curl  -L --fail  'https://bitbucket.org/sivareddyg/hindi-part-of-speech-tagger/downloads/hindi-pos-tagger-3.0.tgz' --output 'hindi-pos-tagger-3.0.tgz'   
tar xvf hindi-pos-tagger-3.0.tgz && rm hindi-pos-tagger-3.0.tgz
patch -p0 < hindi-pos-tagger.patch
rm hindi-pos-tagger-3.0/hindi.input.txt
fi 
