# UD-toolkit
UD-toolkit is an NLP toolkit built around [UDPipe](http://ufal.mff.cuni.cz/udpipe) providing out-of-the-box language tools. Models from [UD 2.0](http://hdl.handle.net/11234/1-2364) are dynamically downloaded so that you can focus on the task at hand.

Note that while this software is licensed under the GPL, the UD 2.0 models are distributed under the [CC BY-NC-SA](http://creativecommons.org/licenses/by-nc-sa/4.0/) license which explictly prohibits commercial use.

# Installation

```
pip install ud-toolkit
```

# Usage

To get started, load a model:

```pycon
>>> from udtk import Model
>>> m = Model("english")
```

UD-toolkit will download the model for you. For a complete list of available model, see `udtk.models.LANGUAGES`.

To tokenize, lemmatize and get part-of-speech tags, ud-toolkit provides easy to use convenience functions.

```pycon
>>> s = "Time flies like an arrow. Fruit flies like a banana."
>>> m.tokenize(s)
['Time', 'flies', 'like', 'an', 'arrow', '.', 'Fruit', 'flies', 'like', 'a', 'banana', '.']
>>> m.lemmatize(s)
['time', 'flie', 'like', 'a', 'arrow', '.', 'fruit', 'fly', 'like', 'a', 'banana', '.']
>>> m.pos_tag(s)
[('Time', 'NOUN'), ('flies', 'VERB'), ('like', 'ADP'), ('an', 'DET'), ('arrow', 'NOUN'), ('.', 'PUNCT'), ('Fruit', 'NOUN'), ('flies', 'VERB'), ('like', 'ADP'), ('a', 'DET'), ('banana', 'NOUN'), ('.', 'PUNCT')]
```

For more advanced usage, you can use `Model.process()`:

```pycon
>>> [(w.lemma, w.xpostag) for w in m.process(s, tag=True)]
[('time', 'NN'), ('flie', 'VBZ'), ('like', 'IN'), ('a', 'DT'), ('arrow', 'NN'), ('.', '.'), ('fruit', 'NN'), ('fly', 'VBZ'), ('like', 'IN'), ('a', 'DT'), ('banana', 'NN'), ('.', '.')]
```

# Supported languages

- ancient_greek
- ancient_greek-proiel
- arabic
- basque
- belarusian
- bulgarian
- catalan
- chinese
- coptic
- croatian
- czech
- czech-cac
- czech-cltt
- danish
- dutch
- dutch-lassysmall
- english
- english-lines
- english-partut
- estonian
- finnish
- finnish-ftb
- french
- french-partut
- french-sequoia
- galician
- galician-treegal
- german
- gothic
- greek
- hebrew
- hindi
- hungarian
- indonesian
- irish
- italian
- japanese
- kazakh
- korean
- latin
- latin-ittb
- latin-proiel
- latvian
- lithuanian
- norwegian-bokmaal
- norwegian-nynorsk
- old_church_slavonic
- persian
- polish
- portuguese
- portuguese-br
- romanian
- russian
- russian-syntagrus
- sanskrit
- slovak
- slovenian
- slovenian-sst
- spanish
- spanish-ancora
- swedish
- swedish-lines
- tamil
- turkish
- ukrainian
- urdu
- uyghur
- vietnamese
