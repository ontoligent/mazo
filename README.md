# Mazo
Mazo is a simple inteface to [MALLET](http://mallet.cs.umass.edu/index.php), built on top of [Polite](https://github.com/ontoligent/polite), which is a lite version of [Polo](https://github.com/ontoligent-design/polo2). Mazo is "mallet" in Spanish and is pronounced `/MA-so/`.

## Installation

First install [MALLET 2.0](https://mimno.github.io/Mallet/). Mazo is a wrapper around MALLET, designed to make it easy to generate topic models and to store the resulting output in a collection of related tables. Ideally, you will have the path to the `mallet` executable in your environment so that it can be run from anywhere on our system.

Then clone this repo and, from within the cloned directory, run `python setup.py install`. This will install the script `mazo` and the library `polite.polite` into your current Python environment. The script `mazo` will be callable from anywhere on your system.

## Usage

Create a working directory for your project and move into it. Create two subdirectories, `./corpus` and `./output` and optionally a configuration file `config.ini`. 

As stated in the installation instructions, Mazo expects `mallet` to be in your `PATH` environment variable. If it is not, you'll need to edit the `config.ini` file. For example, if you are using Windows and followed [the installation instructions](http://mallet.cs.umass.edu/download.php) for MALLET on the website, you'd change the value of `mallet_path` to `bin\mallet`, like so:

```
[DEFAULT]
mallet_path = bin\mallet
``` 

Or, if you want to point to the specific location of `mallet`, you can do something like this:

```
[DEFAULT]
mallet_path = C:\mallet-2.0.8\bin\mallet
```

or 

```
[DEFAULT]
mallet_path = /opt/mallet/bin/mallet
```

To begin using Mazo, you'll need to first put [a MALLET compliant corpus file](http://mallet.cs.umass.edu/import.php) in the corpus directory `./corpus` and name it in a special way:

```
<keyword>-corpus.csv
```

Here, `<keyword>` is a word used to name everything else. For example, the corpus directory contains a sample corpus file called `demo-corpus.csv`; `demo` is the keyword. After mazo runs, everything will be put in an output directory with the word `demo` prefixed to the files and directories.

To run Mazo, do this:

```
mazo <keyword> <k>
```

where `<k>` stands for the number of topics in the model, and `python` is Python 3.*.

To try it out, use the demo file found in the clone repo:

```
mazo demo 20
```

After this runs, in your `./output` directory you will find a directory named someting like this:

```buildoutcfg
output/demo-20-1585231796908834
```
Note, Mazo will create the `./output` if your forgot to.

The long number is just the keyword with the number of tokens and a unix timestamp added to it. It is used to separate your topic models from each other, since each is unique. (You should delete these directories when you done with them.)

Inside of this directory, you will find all the files that MALLET generated, plus a subdirectory `./tables`. In that directory, you should see the following files:

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

Have fun!

# Troubleshooting

One reason `mazo` will fail is that your corpus has characters that are unreadable by `mallet` when it is importing the corpus file. Strip out high-ASCII characters from the file first. You can use the regular expression `[\040-\176]+` to find the offending characters and replacement with the empty string `''`. The MacOS [BBEdit](https://www.barebones.com/products/bbedit/) has a function to do this called "zap gremlins."

# Final Remarks

Mazo is meant to get you started using MALLET and to provide a nice set of output files for downstream analysis, visualization, etc. If you need more power and flexibility, you are encouraged to use MALLET directly. 

If you want to use MALLET directly and then convert the resulting files into relational tables, consider importing `Polite` from `polite.polite` and using it directly. 