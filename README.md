# r/cosplay title crawler

[Available on Kaggle](https://www.kaggle.com/datasets/inhanhv/rcosplay-hot-top-images-with-titles)

Please take time to read all this readme before using the dataset. Yes I'm serious!

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
## Download all posts in top and hot 
(but [the number in each category limited by Reddit](https://stackoverflow.com/a/54046328/13358358))
- Output file: `data/cosplay.jsonl`
- 2161 posts (on 01/03/2023)
```
python rct/crawl.py
```

## Clean text 
(in post's title) enclosed by square brackets such as `[self]`, `[found]`, ... 
- Input file: `data/cosplay.jsonl`
- Output file: `data/clean_cosplay.jsonl`
```
python rct/clean.py
```

## Download images 
- Input file: `data/clean_cosplay.jsonl`
- Output file: `data/map_cosplay.jsonl`, `data/bad_response.jsonl`
- 2160 downloaded images, 1 bad/delete/deprecated image (on 02/03/2023)
```
python rct/download.py
``` 

⚠ The `image_id`, and `image_path` attributes' values are NOT linearly continuous. For example,

in `data/bad_response.jsonl`
```python
{"image_id": "001912", "image_path": "data/image/001912.jpg"}
```
and in `data/map_cosplay.jsonl`
```python
# omit other json objects 
{"image_id": "001911", "image_path": "data/image/001911.jpg"}
{"image_id": "001913", "image_path": "data/image/001913.jpg"}
# omit other json objects
```

⚠ `image_path` attribute's values are `data/image/*.jpg`. They are relative to the folder `data` containing all `.jsonl` files and `image` folder. The folder `data` is produced by Python scripts.

⚠ `image_path` attribute's values MISMATCH with *the name of folder containing all `.jsonl` files and `image` folder on __Kaggle__*. When you load the data from Kaggle Dataset, `"data/image/001912.jpg"`'s `data` should be replaced with Kaggle path (see [this notebook](https://www.kaggle.com/code/inhanhv/rct-demo)).