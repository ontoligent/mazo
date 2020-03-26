# Mazo
Mazo is a simple inteface MALLET, built on top of Polite, which is a lite version of Polo. Mazo is "mallet" in Spanish.

# Instructions

The user puts a MALLET compliant corpus file in the corpus directory and names it in a special way:

```
<keyword>-corpus.csv
```

Here, `<keyword>` is a word used to name everything else. For example, the corpus directory contains a sample corpus file called `demo-corpus.csv`; `demo` is the keyword. After mazo runs, everything will be put in an output directory with the word `demo` prefixed to the files and directories.

To run Mazo the user does this:

```
mazo.py <keyword> <k>
```

where `<k>` stands for the number of topics in the model.

To try it out, use the demo file:

```
python mazo.py demo 20
```

