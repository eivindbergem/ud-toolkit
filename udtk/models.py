import os

from pathlib import Path
from functools import wraps

from .utils import download_file
from .udpipe import load_model, Pipeline, iter_words

LANGUAGES = set(["ancient_greek-proiel", "ancient_greek", "arabic",
                 "basque", "belarusian", "bulgarian", "catalan",
                 "chinese", "coptic", "croatian", "czech-cac",
                 "czech-cltt", "czech", "danish", "dutch-lassysmall",
                 "dutch", "english-lines", "english-partut", "english",
                 "estonian", "finnish-ftb", "finnish", "french-partut",
                 "french-sequoia", "french", "galician-treegal",
                 "galician", "german", "gothic", "greek", "hebrew",
                 "hindi", "hungarian", "indonesian", "irish", "italian",
                 "japanese", "kazakh", "korean", "latin-ittb",
                 "latin-proiel", "latin", "latvian", "lithuanian",
                 "norwegian-bokmaal", "norwegian-nynorsk",
                 "old_church_slavonic", "persian", "polish",
                 "portuguese-br", "portuguese", "romanian",
                 "russian-syntagrus", "russian", "sanskrit", "slovak",
                 "slovenian-sst", "slovenian", "spanish-ancora",
                 "spanish", "swedish-lines", "swedish", "tamil",
                 "turkish", "ukrainian", "urdu", "uyghur", "vietnamese"])

UD_VERSION = "2.0-170801"
MODELS_URL = "https://github.com/eivindbergem/UD-2.0-models/raw/master/"

def get_model_cache_path():
    return MODEL_CACHE

def set_model_cache_path(path):
    global MODEL_CACHE
    MODEL_CACHE = path

def init_model_cache_path():
    try:
        set_model_cache_path(Path(os.environ['UDTK_PATH']))
    except KeyError:
        set_model_cache_path(Path.home() / ".udpipe-models")

init_model_cache_path()

class UnknownLanguageError(Exception):
    def __init__(self, language):
        self.language = language

    def __str__(self):
        return "Unknown language: '{}'".format(self.language)

def assert_valid_language(language):
    if not language in LANGUAGES:
        raise UnknownLanguageError(language)

def ensure_model_loaded(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.model == None:
            self.load_model()
        return fn(self, *args, **kwargs)

    return wrapper

class Model:
    def __init__(self, language):
        assert_valid_language(language)
        self.language = language
        self.model = None

    def load_model(self):
        self.ensure_model_downloaded()
        self.model = load_model(self.get_path())

    def get_path(self):
        return MODEL_CACHE / self.get_model_filename()

    def ensure_model_downloaded(self):
        if not self.get_path().exists():
            self.download_model()

    def get_model_filename(self):
        return "{}-ud-{}.udpipe".format(self.language, UD_VERSION)

    def download_model(self):
        filename = self.get_model_filename()
        url = MODELS_URL + filename

        MODEL_CACHE.mkdir(exist_ok=True)

        download_file(url, MODEL_CACHE / filename)

    def tokenize(self, text):
        return self.process(text, lambda w : w.form)

    def lemmatize(self, text):
        return self.process(text, lambda w : w.lemma, tag=True)

    def pos_tag(self, text, tagset="upostag"):
        return self.process(text,
                            lambda w : (w.form, getattr(w, tagset)),
                            tag=True)

    @ensure_model_loaded
    def process(self, text, fn = lambda w : w, **kwargs):
        pipeline = Pipeline(self.model, "text", **kwargs)

        return [fn(w) for w in iter_words(pipeline.process(text))]
