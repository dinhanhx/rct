# r/cosplay title crawler

# Setup

```
pip install -e .
```

Go to [this PRAW doc page](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#prerequisites), follow the instructions to get your client id, client secret, and user agent.

Then store them in `confidential/reddit.json` like this (don't actually write "spooky"):
```json
{
    "id": "spooky",
    "secret": "spooky",
    "user-agent": "windows-10:spooky:v0.0.1 (by u/spooky)"
}
```

# Run
- Download all posts in top and hot (but [the number in each category limited by Reddit](https://stackoverflow.com/a/54046328/13358358))
- Clean text enclosed by square brackets such as `[self]`, `[found]`, ... 
```
python rct/crawl.py
python rct/clean.py
```

2161 images with captions on 01/03/2023