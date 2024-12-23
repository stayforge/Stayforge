import os.path

import settings


def get_description_md(*path):
    with open(os.path.join(settings.DOCS_API_DESCRIPTION, *path), 'r', encoding='utf-8') as file:
        return file.read()
