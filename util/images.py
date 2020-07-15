import wget
import logging
import time
import json
import os


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger('red.digicord.images')
COURTESY_MS = 2000 # Time in ms between requests
# Directory definitions
FILE_DIR    = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.dirname(FILE_DIR)
IMAGES_DIR  = os.path.join(ROOT_DIR, 'images')
SPRITES_DIR = os.path.join(IMAGES_DIR, 'sprites')
FIELD_DIR   = os.path.join(IMAGES_DIR, 'field')


def get_image(url:str, img_path:str) -> bool:
    """Download image from url to img_path using wget.
    Parameters
    ----------
    url: str
        URL from which to download the image.
    img_path: str
        File path for saving the image. Only tested with absolute paths.
    Returns
    -------
    bool:
        True if download success, else False.
    """
    LOG.debug(f'Downloading {img_path} from {url}')
    if (os.path.isfile(img_path)):
        LOG.debug(f'Found file at {img_path} - removing')
        os.remove(img_path)
    try:
        wget.download(url, img_path, bar=None)
        return True
    except Exception as e:
        LOG.error(f'Problem downloading {url}: {e}')
        return False


# Duplicate functionality from digicord.py
def get_sprite_path(species_number:int, digits:int=3) -> str:
    """Generate sprite image path for given species_number.
    Parameters
    ----------
    species_number: int
        Species number of the Digimon.
    digits: int, optional
        Number of digits in the file name for leading zeros, default 3.
    """
    # This syntax for the leading zeroes is not very readable but works
    return os.path.join(SPRITES_DIR, f'sprite-{species_number:0{digits}d}.png')


# Duplicate functionality from digicord.py
def get_field_path(species_number:int, digits:int=3) -> str:
    """Generate field image path for given species_number.
    Parameters
    ----------
    species_number: int
        Species number of the Digimon.
    digits: int, optional
        Number of digits in the file name for leading zeros, default 3.
    """
    # This syntax for the leading zeroes is not very readable but works
    return os.path.join(FIELD_DIR, f'field-{species_number:0{digits}d}.png')


if __name__ == '__main__':
    """Download sprite and field images from database entries
    """
    database        = json.load(open('database.json'))
    first_download  = True
    for digimon in database:
        if (not first_download):
            time.sleep(COURTESY_MS / 1000)
        first_download = False
        sprite_path = get_sprite_path(digimon['species_number'])
        field_path  = get_field_path(digimon['species_number'])
        get_image(digimon['sprite_url'], sprite_path)
        time.sleep(COURTESY_MS / 1000)
        get_image(digimon['field_url'], field_path)

    LOG.debug('Done downloading images')

