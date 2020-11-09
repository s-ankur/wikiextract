get_seeded_random()
{
  seed="$1"
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}

shuf $1".src" --random-source=<(get_seeded_random $2)>tmp.src
shuf $1".tgt" --random-source=<(get_seeded_random $2)>tmp.tgt

mv tmp.src $1".src" 
mv tmp.tgt $1".tgt" 
