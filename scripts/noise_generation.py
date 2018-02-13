# coding=utf-8
from __future__ import unicode_literals

import argparse
import io
import operator
import os
from collections import defaultdict

import numpy as np
import pandas as pd
from future.builtins import str, range
from future.utils import itervalues, iteritems
from wordfreq import word_frequency, iter_wordlist

from scripts.utils import SCRIPTS_PATH


def sample_words(words_frequencies, n_samples, truncate=None):
    words, probs = zip(*sorted(words_frequencies.items(),
                               key=operator.itemgetter(1), reverse=True))
    if truncate:
        words = words[:truncate]
        sum_probs = sum(probs[:truncate])
        probs = [p / sum_probs for p in probs[:truncate]]
    return np.random.choice(words, size=n_samples, p=probs)


def load_en_words_frequencies():
    path = os.path.join(SCRIPTS_PATH, "words_frequencies", "count_en.txt")
    sep = "\t"
    freqs = dict()
    with io.open(path, "r", encoding="utf8") as f:
        for line in f:
            split = line.split(sep)
            if len(split) != 2:
                continue
            word, freq = split
            if word in freqs:
                continue
            freqs[word] = float(freq)
    total = float(sum(freqs.values()))
    freqs = {k: v / total for k, v in iteritems(freqs)}
    return freqs


def load_de_words_frequencies():
    path = os.path.join(SCRIPTS_PATH, "words_frequencies", "count_de.txt")
    df = pd.read_csv(path, sep="\t", header=0, index_col=None,
                     encoding="latin-1")
    df["WFfreqcount"] /= float(sum(df["WFfreqcount"]))
    freqs = defaultdict(float)
    for row in df.itertuples():
        freqs[row.Word.lower()] += row.WFfreqcount
    return freqs


def load_es_words_frequencies():
    path = os.path.join(SCRIPTS_PATH, "words_frequencies", "count_es.txt")
    cols = ["Word0", "Word1", "Word2", "Freq. count0", "Freq. count1",
            "Freq. count2"]
    df = pd.read_csv(path, sep=";", header=0, index_col=None, encoding="utf8",
                     usecols=cols)
    to_concat = []
    for i in range(3):
        col_word = "Word{}".format(i)
        col_freq = "Freq. count{}".format(i)
        df_freq = df[[col_word, col_freq]]
        df_freq = df_freq.rename(columns={col_word: "word", col_freq: "freq"})
        to_concat.append(df_freq)
    df_freqs = pd.concat(to_concat).dropna()
    df_freqs["freq"] /= float(sum(df_freqs["freq"]))
    freqs = defaultdict(float)
    for row in df_freqs.itertuples():
        freqs[str(row.word).lower()] += row.freq
    return freqs


def load_zh_words_frequencies():
    path = os.path.join(SCRIPTS_PATH, "words_frequencies", "count_zh.txt")
    cols = ["Word", "WCount"]
    df = pd.read_csv(path, sep=";", header=2, index_col=None, encoding="utf8",
                     usecols=cols)
    df["WCount"] /= float(sum(df["WCount"]))
    freqs = defaultdict(float)
    for row in df.itertuples():
        freqs[str(row.Word).lower()] += row.WCount
    return freqs


def load_fr_words_frequencies():
    path = os.path.join(SCRIPTS_PATH, "words_frequencies", "count_fr.txt")
    sep = " "
    freqs = dict()
    with io.open(path, "r", encoding="utf8") as f:
        for line in f:
            split = line.split(sep)
            if len(split) != 2:
                continue
            word, freq = split
            if word in freqs:
                continue
            freqs[word] = float(freq)
    total = float(sum(freqs.values()))
    freqs = {k: v / total for k, v in iteritems(freqs)}
    return freqs


def default_words_frequencies(language):
    freqs = {w: word_frequency(w, language) for w in iter_wordlist(language)}
    total = float(sum(itervalues(freqs)))
    return {k: v / total for k, v in iteritems(freqs)}


def load_words_frequencies(language):
    if language == "en":
        words_frequencies = load_en_words_frequencies()
    elif language == "de":
        words_frequencies = load_de_words_frequencies()
    elif language == "es":
        words_frequencies = load_es_words_frequencies()
    elif language == "zh":
        words_frequencies = load_zh_words_frequencies()
    elif language == "fr":
        words_frequencies = load_fr_words_frequencies()
    else:
        try:
            words_frequencies = default_words_frequencies(language)
        except OSError:
            raise RuntimeError("Properly install mecab")
        except LookupError:
            raise OSError("Unknown language: %s" % language)
    return words_frequencies


def generate_noise(language, n_words, output_path, truncate=None):
    words_frequencies = load_words_frequencies(language)
    samples = sample_words(words_frequencies, n_words, truncate)
    with io.open(output_path, "w", encoding="utf8") as f:
        f.write(" ".join(samples))
    print("Wrote noise to {}".format(output_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate noise from a words frequency")
    parser.add_argument("language", type=str)
    parser.add_argument("n_words", type=int)
    parser.add_argument("output_path", type=str)
    parser.add_argument("--truncate", type=int)
    args = parser.parse_args()
    generate_noise(**vars(args))
