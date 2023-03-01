import re
from pathlib import Path

import jsonlines as jsonl
from tqdm import tqdm


COSPLAY_JSONL = Path('data/cosplay.jsonl')
CLEAN_COSPLAY_JSONL = Path('data/clean_cosplay.jsonl')

with (jsonl.open(COSPLAY_JSONL, 'r') as cosplay_fp,
      jsonl.open(CLEAN_COSPLAY_JSONL, 'a') as clean_cosplay_fp):
    for d in tqdm(cosplay_fp):
        # Regex \[(.*?)\] or \[.*\] to detect text enclosed by square brackets
        # such as [self]
        d['caption'] = re.sub(r'\[(.*?)\]', '', d['caption'])
        clean_cosplay_fp.write(d)
