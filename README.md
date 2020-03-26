# Mazo
Mazo is a simple inteface MALLET, built on top of Polite, which is a lite version of Polo. Mazo is "mallet" in Spanish.

# Instructions

Mazo expects `mallet` to be in your PATH environment variable. 

The user puts a MALLET compliant corpus file in the corpus directory and names it in a special way:

```
<keyword>-corpus.csv
```

Here, `<keyword>` is a word used to name everything else. For example, the corpus directory contains a sample corpus file called `demo-corpus.csv`; `demo` is the keyword. After mazo runs, everything will be put in an output directory with the word `demo` prefixed to the files and directories.

To run Mazo the user does this:

```
python mazo.py <keyword> <k>
```

where `<k>` stands for the number of topics in the model, and `python` is Python 3.*. (Note, if you know how to use `chmod`, you don't need to call Python explicitly.)

To try it out, use the demo file:

```
python mazo.py demo 20
```

After this runs, you should see and `output` directory. In that, you will see a directory named someting like this:

```buildoutcfg
output/demo-1585231796908834
```

That number is just a unix timestamp. It is used to separate your topic models from each other, sinc each is unique. You should delete these directories when you done with them.

Inside this directory, you will find all the files that MALLET generated, plus a directory called `tables`. In that directory, you should see the following files:

```buildoutcfg
DOC.csv
DOCTOPIC.csv
DOCTOPIC_NARROW.csv
DOCWORD.csv
TOPIC.csv
TOPICPHRASE.csv
TOPICWORD.csv
TOPICWORD_DIAGS.csv
TOPICWORD_NARROW.csv
TOPICWORD_WEIGHTS.csv
VOCAB.csv
```

These files implement a relational data model of the topic model. They can be imported into a relational database (like SQLite) or read directly into Pandas.  

