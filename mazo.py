#!/usr/bin/env python3

import sys, os, re
import configparser
from polite.polite import Polite

mazo_config = configparser.ConfigParser()
mazo_config.read('config.ini')
mallet_bin = mazo_config['DEFAULT']['mallet_path']
mallet_output_dir = mazo_config['DEFAULT']['output_dir']
print("Using {} as mallet.".format(mallet_bin))
print("Using {} as output directory.".format(mallet_output_dir))

# Get keyword
try:
    keyword = sys.argv[1]
except IndexError:
    print("Please provide a keyword for your corpus.")
    sys.exit()

# Get number of topics
try:
    n_topics = int(sys.argv[2])
    if n_topics > 500:
        print("That's a large number of topics. Try a smaller number.")
        sys.exit()
except ValueError:
    print("Please enter an integer for the number of topics.")
    sys.exit()
except IndexError:
    print("No value provided for number of topics. Using 10.")
    n_topics = 10

# See if a corpus file exists. If not, complain.
corpus_file = "corpus/{}-corpus.csv".format(keyword)
if not os.path.isfile(corpus_file):
    print("Corpus file {} not found.".format(corpus_file))
    sys.exit()

# See if corpus file has been imported
mallet_file = "corpus/{}-corpus.mallet".format(keyword)
if not os.path.isfile(mallet_file):
    print("MALLET file {} not found. Creating it now.".format(mallet_file))
    cmd = "{} import-file --input {} --output {} --keep-sequence true --remove-stopwords true"\
        .format(mallet_bin, corpus_file, mallet_file)
    os.system(cmd)
    print("Done creating MALLET file.")

# Make sure output directory exists
if not os.path.isfile(mallet_output_dir):
    try:
        os.mkdir(mallet_output_dir)
    except FileExistsError:
        pass

# Create trial directory
import time
trial_key = str(time.time()).replace('.', '')
mallet_trial_dir = "{}/{}-{}".format(mallet_output_dir, keyword, trial_key)
print("Creating output directory {}".format(mallet_trial_dir))
if not os.path.isfile(mallet_trial_dir):
    try:
        os.mkdir(mallet_trial_dir)
    except FileExistsError:
        pass

# Run the topic model
# todo: Eventually provide ways to override these defaults
print("Running topic model.")
params = {
    'num-topics': n_topics,
    'num-top-words': 10,
    'num-iterations': 1000,
    'optimize-interval': 100,
    'num-threads': 4,
    'num-top-docs': 5,
    'doc-topics-max': 10,
    'show-topics-interval': 100,
    'input': mallet_file,
    'output-topic-keys': '{}/topic-keys.txt'.format(mallet_trial_dir),
    'output-doc-topics': '{}/doc-topics.txt'.format(mallet_trial_dir),
    'word-topic-counts-file': '{}/word-topic-counts.txt'.format(mallet_trial_dir),
    'topic-word-weights-file': '{}/topic-word-weights.txt'.format(mallet_trial_dir),
    'xml-topic-report': '{}/topic-report.xml'.format(mallet_trial_dir),
    'xml-topic-phrase-report': '{}/topic-phrase-report.xml'.format(mallet_trial_dir),
    'diagnostics-file': '{}/diagnostics.xml'.format(mallet_trial_dir),
    'output-state': '{}/output-state.gz'.format(mallet_trial_dir)
}
cmds = []
for k, v in params.items():
    cmds.append("--{} {}".format(k, v))
train_cmd = "{} train-topics ".format(mallet_bin) + ' '.join(cmds)
print("Command to be executed.")
print(train_cmd)
os.system(train_cmd)
print("Done with training model.")

# Make trial config file
mallet_trial_config = "{}/.config.txt".format(mallet_trial_dir)
print("Printing config file {}.".format(mallet_trial_config))
with open(mallet_trial_config, 'w') as cfg_file:
    for k, v in params.items():
        cfg_file.write("{} {}\n".format(k, v))

# Convert MALLET outpupt files to tables
tables_dir = "{}/tables".format(mallet_trial_dir)
print("Putting tables in {}".format(tables_dir))
if not os.path.isfile(tables_dir):
    try:
        os.mkdir(tables_dir)
    except FileExistsError:
        pass

# Run Polite
p = Polite(mallet_trial_config, tables_dir+'/')
p.do_all()

print("Done.")

