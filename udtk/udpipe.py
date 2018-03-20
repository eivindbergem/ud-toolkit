from functools import reduce

import ufal.udpipe

class UDPipeError(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return self.err

def read_sentences(input_format, data):
    """Read sentences into input format from data."""

    # Input text
    input_format.setText(data)

    # Errors will show up here
    error = ufal.udpipe.ProcessingError()

    # Create empty sentence
    sentence = ufal.udpipe.Sentence()

    # Fill sentence object
    while input_format.nextSentence(sentence, error):
        # Check for error
        if error.occurred():
            raise UDPipeError(error.message)

        yield sentence

        sentence = ufal.udpipe.Sentence()

def iter_words(sentences):
    for s in sentences:
        for w in s.words[1:]:
            yield w

class Pipeline(object):
    def __init__(self, model, input_format, output_format=None,
                 tag=False, parse=False):
        self.model = model
        tokenizer = model.newTokenizer(model.DEFAULT)

        INPUT_FORMATS = {"text": lambda x : read_sentences(tokenizer, x)}

        self.pipes = [INPUT_FORMATS[input_format]]

        if tag:
            self.pipes.append(self.tag)

    def tag(self, sentences):
        """Tag sentences adding lemmas, pos tags and features for each token."""

        for sentence in sentences:
            self.model.tag(sentence, self.model.DEFAULT)
            yield sentence

    def process(self, inputs):
        for fn in self.pipes:
            inputs = fn(inputs)

        return inputs

def load_model(filename):
    return ufal.udpipe.Model.load(str(filename))
