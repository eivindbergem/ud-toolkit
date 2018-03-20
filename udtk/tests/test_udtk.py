import hashlib
import shutil

from pathlib import Path
from unittest import TestCase
from tempfile import mkdtemp

import udtk
from udtk.utils import download_file
from udtk import Model
from udtk.models import get_model_cache_path, set_model_cache_path

TEST_URL = "http://www.gutenberg.org/files/1342/1342-0.txt"
TEST_CHECKSUM= "48e0522844402a86a3ea98f0947ba85ea54838db3c59022299298ed968a5a163"
TEST_LANGUAGE = "lithuanian"
TEST_SENTENCE = "Vikipedija yra interneto enciklopedija, kurią nemokamai ir be jokių apribojimų gali skaityti, tobulinti ir pildyti visi žmonės. Vikipediją galima skaityti daugiau nei dviem šimtais kalbų, o lietuviškuosiuose puslapiuose jau yra daugiau nei 187 tūkstančiai straipsnių ir jų skaičius nuolat auga."
TEST_POS = [('Vikipedija', 'NOUN'), ('yra', 'AUX'), ('interneto', 'NOUN'),
            ('enciklopedija', 'NOUN'), (',', 'PUNCT'), ('kurią', 'PRON'),
            ('nemokamai', 'VERB'), ('ir', 'CCONJ'), ('be', 'ADP'),
            ('jokių', 'DET'), ('apribojimų', 'NOUN'), ('gali', 'VERB'),
            ('skaityti', 'VERB'), (',', 'PUNCT'), ('tobulinti', 'VERB'),
            ('ir', 'CCONJ'), ('pildyti', 'VERB'), ('visi', 'DET'),
            ('žmonės', 'NOUN'), ('.', 'PUNCT'), ('Vikipediją', 'PRON'),
            ('galima', 'VERB'), ('skaityti', 'VERB'), ('daugiau', 'ADV'),
            ('nei', 'CCONJ'), ('dviem', 'ADV'), ('šimtais', 'PROPN'),
            ('kalbų', 'NOUN'), (',', 'PUNCT'), ('o', 'CCONJ'),
            ('lietuviškuosiuose', 'DET'), ('puslapiuose', 'NOUN'),
            ('jau', 'PART'), ('yra', 'AUX'), ('daugiau', 'ADV'),
            ('nei', 'CCONJ'), ('187', 'NUM'), ('tūkstančiai', 'ADV'),
            ('straipsnių', 'NOUN'), ('ir', 'CCONJ'), ('jų', 'DET'),
            ('skaičius', 'NOUN'), ('nuolat', 'ADV'), ('auga', 'VERB'),
            ('.', 'PUNCT')]
TEST_LEMMA = ['Vikipedija', 'būti', 'internesti', 'enciklopedija', ',',
              'kuris', 'mokamai', 'ir', 'be', 'joks', 'apribojimas', 'galėti',
              'skaityti', ',', 'tobulinti', 'ir', 'pildyti', 'visas', 'žmonė',
              '.', 'Vikipediji', 'galėti', 'skaityti', 'daug', 'nei', 'dviem',
              'šimtas', 'kalba', ',', 'o', 'lietuviškuosiui', 'puslapiui',
              'jau', 'būti', 'daug', 'nei', '187', 'tūkstančiai', 'straipsnis',
              'ir', 'jų', 'skaičis', 'nuolat', 'augti', '.']

def get_hash(filename, block_size=2**13):
    m = hashlib.sha256()

    with filename.open("rb") as fd:
        while True:
            block = fd.read(block_size)

            if not block:
                break

            m.update(block)

    return m.hexdigest()

class TestUdtk(TestCase):
    def setUp(self):
        self.path = Path(mkdtemp())
        set_model_cache_path(self.path)

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_utils(self):
        filename = self.path / "test-file.txt"

        download_file(TEST_URL, filename)

        self.assertEqual(get_hash(filename), TEST_CHECKSUM)

    def test_model(self):
        m = Model(TEST_LANGUAGE)
        self.assertEqual(get_model_cache_path(), self.path)

        self.assertEqual(m.lemmatize(TEST_SENTENCE), TEST_LEMMA)
        self.assertEqual(m.pos_tag(TEST_SENTENCE), TEST_POS)
