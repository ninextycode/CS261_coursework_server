import inspect
import os


keys_dir = os.path.join(os.path.join(os.path.join(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                os.pardir), os.pardir), 'keys')

twitter_key_path = os.path.join(keys_dir, 'twitter_key.json')
summariser_key_path = os.path.join(keys_dir, 'summariser_key.txt')
google_key_path = os.path.join(keys_dir, 'google_key.json')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_key_path


import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')