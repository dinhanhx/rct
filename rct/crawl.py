import json
from pathlib import Path
from typing import Final

import jsonlines as jsonl
import praw
from tqdm import tqdm

from rct.image_text import ImageCaption

CONFIDENTIAL_PATH: Final[Path] = Path('confidential/reddit.json')
DATA_PATH: Final[Path] = Path('data')
IMAGE_FMT: Final[tuple] = ('.jpg', '.png', '.jpeg')

with open(CONFIDENTIAL_PATH) as fp:
    reddit_config = json.load(fp)

reddit_client = praw.Reddit(
    client_id=reddit_config['id'],
    client_secret=reddit_config['secret'],
    user_agent=reddit_config['user-agent'],
)
print(f'Reddit client read_only: {reddit_client.read_only}')

with jsonl.open(DATA_PATH.joinpath('cosplay.jsonl'), 'r') as fp:
    id_set = set()
    for d in fp:
        id_set.add(d['submission_id'])
print(f'Current number of submissions: {len(id_set)}')

subreddit_iterator_dict = {
    'hot': reddit_client.subreddit('cosplay').hot,
    'top': reddit_client.subreddit('cosplay').top
}

for key in subreddit_iterator_dict:
    for submission in tqdm(subreddit_iterator_dict[key](limit=None)):
        if submission.id in id_set:  # ignore already-crawled submissions
            continue

        if submission.is_self:  # ignore text-only submissions
            continue

        if submission.url.endswith(IMAGE_FMT):  # handle single-image submission
            ic = ImageCaption(
                image_url=submission.url,
                caption=submission.title,
                article_url=f'https://www.reddit.com{submission.permalink}',
                submission_id=submission.id
            )
            with jsonl.open(DATA_PATH.joinpath('cosplay.jsonl'), 'a') as fp:
                fp.write(ic.to_dict())

        if submission.url.startswith('https://www.reddit.com/gallery'):  # handle multiple-image submission
            for _, image_item in submission.media_metadata.items():
                ic = ImageCaption(
                    image_url=image_item['s']['u'],
                    caption=submission.title,
                    article_url=f'https://www.reddit.com{submission.permalink}',
                    submission_id=submission.id
                )
                with jsonl.open(DATA_PATH.joinpath('cosplay.jsonl'), 'a') as fp:
                    fp.write(ic.to_dict())
