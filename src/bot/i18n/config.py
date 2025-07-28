import os
from pathlib import Path

from modern_i18n.i18n import I18n

project_root = Path(__file__).resolve().parent.parent.parent
LOCALE_PATH = os.path.join(project_root, 'locales')

config = {
    'locale_path': LOCALE_PATH,  
    'locales': ['ru', 'en'],  
    'default_locale': 'ru',  
    'default_encoding': 'UTF-8' 
}

i18n = I18n(config)
t = i18n.translate

__all__ = ["t"]