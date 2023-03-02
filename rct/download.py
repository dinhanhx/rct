from io import BytesIO
from pathlib import Path

import jsonlines as jsonl
import urllib3
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

from rct.image_text import ImageCaptionPath
from rct.delay_keyboard_interupt import DelayedKeyboardInterrupt

COSPLAY_IMAGE_PATH = Path('data/image')
COSPLAY_IMAGE_PATH.mkdir(exist_ok=True)
CLEAN_COSPLAY_JSONL = Path('data/clean_cosplay.jsonl')
MAP_COSPLAY_JSONL = Path('data/map_cosplay.jsonl')  # store list of ImageCaptionPath
BAD_RESPONSE_JSONL = Path('data/bad_response.jsonl')  # store list of ImageCaptionPath when image cannot be downloaded
DOWNLOAD_CKPT = Path('data/download_ckpt.txt')

with open(DOWNLOAD_CKPT, 'r') as fp:
    i_ckpt = int(fp.readline().strip('\n'))
print(f'Resume download after {str(i_ckpt).zfill(6)}.jpg')

http = urllib3.PoolManager()

with (
    jsonl.open(CLEAN_COSPLAY_JSONL, 'r') as clean_cosplay_fp,
    jsonl.open(MAP_COSPLAY_JSONL, 'a') as map_cosplay_fp,
    jsonl.open(BAD_RESPONSE_JSONL, 'a') as bad_response_fp
):
    for i, d in enumerate(tqdm(clean_cosplay_fp)):
        if i <= i_ckpt:  # After i_ckpt.jgp, resume download
            continue

        image_id = str(i).zfill(6)
        image_path = COSPLAY_IMAGE_PATH.joinpath(f'{image_id}.jpg')

        response = http.request('GET', d['image_url'])
        image_data = BytesIO(response.data)

        # sometimes, people post direct image links (hosted by other platform) on reddit
        # hence, these images can be deleted/deprecated by other platform
        # then, response.data is bad
        try:
            image = Image.open(image_data)
        except UnidentifiedImageError:
            bad_response_fp.write(
                ImageCaptionPath(
                    image_url=d['image_url'],
                    caption=d['caption'],
                    article_url=d['article_url'],
                    submission_id=d['submission_id'],
                    image_id=image_id,
                    image_path=image_path.as_posix()  # create posix path on Windows systems
                ).to_dict()
            )

            with open(DOWNLOAD_CKPT, 'w') as download_ckpt_fp:
                download_ckpt_fp.write(image_id)
            continue

        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
        image = image.convert('RGB') if image.mode == 'RGBA' else image
        image = image.convert('RGB') if image.mode == 'P' else image

        with DelayedKeyboardInterrupt():
            image.save(str(image_path))

            map_cosplay_fp.write(
                ImageCaptionPath(
                    image_url=d['image_url'],
                    caption=d['caption'],
                    article_url=d['article_url'],
                    submission_id=d['submission_id'],
                    image_id=image_id,
                    image_path=image_path.as_posix()  # to create posix path on Windows systems
                ).to_dict()
            )

            with open(DOWNLOAD_CKPT, 'w') as download_ckpt_fp:
                download_ckpt_fp.write(image_id)
