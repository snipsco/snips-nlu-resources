# coding=utf-8
from __future__ import unicode_literals

import io

import fire
import spacy


def compute_clusters(language):
    nlp = spacy.load(language)
    clusters = dict()
    for t in nlp.vocab:
        clusters[t.lower_] = unicode(t.cluster)
    return clusters


def main_compute_clusters(language, output_path):
    clusters = compute_clusters(language)
    string_clusters = "\n".join(
        "{}\t{}".format(w, c) for w, c in clusters.iteritems())
    with io.open(output_path, "w", encoding="utf8") as f:
        f.write(string_clusters)


if __name__ == "__main__":
    fire.Fire(main_compute_clusters)
