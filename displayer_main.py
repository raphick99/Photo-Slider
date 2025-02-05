import logging
import pathlib
import subprocess

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# DOWNLOADS_DIR = pathlib.Path('/tmp/downloads')
DOWNLOADS_DIR = pathlib.Path('./downloads')
SLIDESHOW_DELAY = 1


def display_photos():
    while True:
        dirlist = list(DOWNLOADS_DIR.glob('*'))
        if not dirlist:
            logger.info('No files yet, continueing..')
            continue

        command = (
            'feh '
            '--auto-zoom '
            '--fullscreen '
            '--borderless '
            '--hide-pointer '  # check that this works
            f'--slideshow-delay={SLIDESHOW_DELAY} '
            f'{" ".join(str(path) for path in dirlist)}'
        )
        logger.info(f'executing: {command}')
        subprocess.run(command, shell=True)


def main():
    logger.info('starting to display photos..')
    try:
        display_photos()
    except BaseException as e:
        logger.error(f'caught exception! {e}')


if __name__ == "__main__":
    main()