import ufal.udpipe

class UDPipeError(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return self.err

def iter_words(sentences):
    for s in sentences:
        for w in s.words[1:]:
            yield w

class Pipeline(object):
    def __init__(self, input_format, model=None, output_format=None, output_stream=None,
                 tag=False, parse=False):
        self.model = model

        if model:
            self.input_format = model.newTokenizer(model.DEFAULT)
        else:
            self.input_format = ufal.udpipe.InputFormat.newInputFormat(input_format)

        self.pipes = []

        self.pipes.append(self.read_input)

        if tag:
            self.pipes.append(self.tag)

        if output_format:
            self.output_format = ufal.udpipe.OutputFormat.newOutputFormat(output_format)
            self.output_stream = output_stream
            self.pipes.append(self.write_output)

    def read_input(self, data):
        # Input text
        self.input_format.setText(data)

        # Errors will show up here
        error = ufal.udpipe.ProcessingError()

        # Create empty sentence
        sentence = ufal.udpipe.Sentence()

        # Fill sentence object
        while self.input_format.nextSentence(sentence, error):
            # Check for error
            if error.occurred():
                raise UDPipeError(error.message)

            yield sentence

            sentence = ufal.udpipe.Sentence()

    def tag(self, sentences):
        """Tag sentences adding lemmas, pos tags and features for each token."""

        for sentence in sentences:
            self.model.tag(sentence, self.model.DEFAULT)
            yield sentence

    def write_output(self, sentences):
        output = ""

        for sentence in sentences:
            output += self.output_format.writeSentence(sentence)

        output += self.output_format.finishDocument()

        return output

    def process(self, inputs):
        for fn in self.pipes:
            inputs = fn(inputs)

        return inputs

def load_model(filename):
    return ufal.udpipe.Model.load(str(filename))
