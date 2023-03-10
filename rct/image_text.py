from dataclasses import dataclass

from dataclass_wizard import JSONWizard
from dataclass_wizard.enums import LetterCase


@dataclass
class ImageCaption(JSONWizard):
    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_load = LetterCase.SNAKE
        key_transform_with_dump = LetterCase.SNAKE

    # These 3 fields must match the one in image_text.py in dinhanhx/vcc
    image_url: str
    caption: str
    article_url: str

    # Reddit id
    submission_id: str


@dataclass
class ImageCaptionPath(ImageCaption, JSONWizard):
    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_load = LetterCase.SNAKE
        key_transform_with_dump = LetterCase.SNAKE

    image_id: str  # 6 digits e.g 000420
    image_path: str  # image/image_id.jpg e.g image/000420.jpg
