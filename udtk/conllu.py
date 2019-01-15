from .udpipe import Pipeline

class ConlluFile(object):
    def __init__(self, filename):
        self.filename = filename

    def to_text(self, tokenized=False):
        if tokenized:
            output_format = "horizontal"
        else:
            output_format = "plaintext"

        pipeline = Pipeline("conllu", output_format=output_format)

        output = []
        buf = []

        with open(self.filename) as fd:
            for line in fd:
                if line.strip():
                    buf.append(line)
                elif buf:
                    output.append(pipeline.process("".join(buf)))
                    buf = []

        if buf:
            output.append(pipeline.process("".join(buf)))

        return "".join(output)
