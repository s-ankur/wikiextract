# wikiextract

This package is used to create an artificial dataset of Hindi Errors. It depends on the wikiextractor package from here: https://github.com/attardi/wikiextractor.
It does the following:

1. Downloads a "current" hindi wikipedia dump. Note that it can use any corpus of hindi sentences, such as HindiMonocorp, but we have not tried to do that
2. Extracts meaningful sentences from the wikipedia dump 
3. Taking these as 'correct' sentences, it creates erroneous sentences using some heuristics and rule based algorithms (see insert_error.py)
4. For error correction task the erroneous sentences are considered as source file and  the correct sentences are considered as the target files

To run, simply: 

1. run `bash setup.sh`
2. run `bash run_hiwiki.sh` 
3. optionally 

Note that you may need to update a link inside setup.sh, since wikimedia deletes old dumps.

We do not consider spelling errors to be grammatical errors and as such avoid generating spelling errors. Still, due to inadequacies in the POS tagger that we use, we still generate some spelling errors regardless. In fact much of the code in insert_error.py is based around circumventing these inadequacies.

The ouput of `run_hiwiki.sh` is a file `hiwiki.augmented.edits` which contains the parallel corpus of hindi errors in the .edits format. You can convert it to whatever format you like using the tools in `scripts/`.

