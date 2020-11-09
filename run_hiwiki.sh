#!/bin/bash
set -e
set -x
SEED=42
OUTPUT_SENT=1000000

# downloaded from Wikimedia dumps
HIWIKI_FILE='hiwiki-pages-meta-current.xml'

# if you have already extracted you can point EXTRACTED_FILE to it otherwise let it be
EXTRACTED_FILE='extracted'


get_seeded_random()
{
  openssl enc -aes-256-ctr -pass pass:"$1" -nosalt \
    </dev/zero 2>/dev/null
}


EXTRACT_TEXT='python3 WikiExtractor.py --quiet --no_templates --filter_disambig_pages   --min_text_length 20   $HIWIKI_FILE -b 5G -o -'
TOKENIZE_SENTENCE='python3 indic_sentence_tokenizer.py'
SELECT_RANDOM_SENTENCE='shuf -n $OUTPUT_SENT --random-source=<(get_seeded_random $SEED)'
INSERT_ERRORS='python3 insert_errors.py hindi.output  --single --edits'


if [ ! -f $EXTRACTED_FILE ]; then
    eval "$EXTRACT_TEXT>$EXTRACTED_FILE" 
fi

if [ -f $EXTRACTED_FILE ] && [ ! -f hindi-pos-tagger-3.0/hindi.input.txt ]; then
    wc -l $EXTRACTED_FILE
    eval "$TOKENIZE_SENTENCE<$EXTRACTED_FILE>tmp.tok"
    eval $SELECT_RANDOM_SENTENCE<tmp.tok>hindi.input.txt
    wc -l hindi.input.txt
    rm tmp.tok
    mv hindi.input.txt hindi-pos-tagger-3.0/hindi.input.txt
fi

if [ -f hindi-pos-tagger-3.0/hindi.input.txt ] && [ ! -f hindi.output ]; then
    cd hindi-pos-tagger-3.0
    make tag
    wc -l hindi.output
    cd ..
    mv hindi-pos-tagger-3.0/hindi.output hindi.output
fi

eval "$INSERT_ERRORS>hiwiki.augmented.edits"

