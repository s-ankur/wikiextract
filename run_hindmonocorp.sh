#!/bin/bash
set -e
set -x

SEED=42


get_seeded_random()
{
  openssl enc -aes-256-ctr -pass pass:"$1" -nosalt \
    </dev/zero 2>/dev/null
}

UNZIP='gzip -cd hindmonocorp05.plaintext.gz'
EXTRACT='python3 HindmonoExtractor.py'
TOKENIZE_SENTENCE='python3 indic_sentence_tokenizer.py'
SELECT_RANDOM_SENTENCE='shuf --random-source=<(get_seeded_random $SEED)'

eval "$UNZIP|$EXTRACT|$TOKENIZE_SENTENCE>temp"
eval "$SELECT_RANDOM_SENTENCE temp > train_himono.tgt"
rm temp
