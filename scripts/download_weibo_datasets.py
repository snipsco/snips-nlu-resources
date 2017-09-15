# coding=utf-8
from __future__ import unicode_literals

import argparse
import csv
import io
import os
import shutil
import string
import tempfile
import urllib
import zipfile

import pandas as pd
from zhon import hanzi

LEIDEN_CORPUS_URL = "http://lwc.daanvanesch.nl/download.php?file=messages"

CORPUSES = {"leiden"}

MANDARIN_PUNCTUATION = string.punctuation + hanzi.punctuation


def filter_punctuation(message):
    return " ".join(
        t for t in message.split() if t not in MANDARIN_PUNCTUATION)


def download_leiden_weibo_corpus(output_path):
    tmp_dir_path = tempfile.mkdtemp()
    try:
        archive_path = os.path.join(tmp_dir_path, "archive.zip")
        urllib.urlretrieve(LEIDEN_CORPUS_URL, archive_path)

        dir_path = os.path.join(tmp_dir_path, "archive")
        zip_ref = zipfile.ZipFile(archive_path, 'r')
        zip_ref.extractall(dir_path)
        zip_ref.close()

        message_path = os.path.join(dir_path, "parsed_messages.txt")
        df = pd.read_csv(message_path, encoding="utf8", sep=",",
                         index_col=None, quoting=csv.QUOTE_ALL,
                         error_bad_lines=False, header=None)
        message_col = 7
        messages = [
            m for m in df[df[message_col] != "\\N"][message_col].dropna()]
        messages = [filter_punctuation(m) for m in messages]
        with io.open(output_path, "w", encoding="utf8") as f:
            f.write("\n".join(messages))
    finally:
        shutil.rmtree(tmp_dir_path)


def main_download_weibo_datasets():
    parser = argparse.ArgumentParser(
        description="Downloads Weibo corpus, preprocess it and save it")
    parser.add_argument("corpus", choices=CORPUSES)
    parser.add_argument("output_path")
    args = vars(parser.parse_args())
    corpus = args.pop("corpus")
    if corpus == "leiden":
        download_leiden_weibo_corpus(**args)
    else:
        raise ValueError("Invalid corpus '%s', valid corpus are: %s"
                         % (corpus, CORPUSES))


if __name__ == '__main__':
    main_download_weibo_datasets()
