# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import io
import operator
import time
from itertools import izip

from gensim.models import KeyedVectors
from sklearn.cluster import KMeans


def compute_clusters(word_vectors, n_clusters):
    start = time.time()
    kmeans_clustering = KMeans(n_clusters=n_clusters, n_jobs=2)
    idx = kmeans_clustering.fit_predict(word_vectors.syn0)
    end = time.time()
    elapsed = end - start
    print("Computed clusters in: %s seconds" % elapsed)
    clusters = dict(izip(word_vectors.index2word, idx))
    return clusters


def load_word_vectors(vectors_path):
    start = time.time()
    vectors = KeyedVectors.load_word2vec_format(vectors_path, binary=True)
    end = time.time()
    elapsed = end - start
    print("Loaded word vectors in: %s seconds" % elapsed)
    return vectors


def save_word_clusters(clusters, path):
    with io.open(path, "w", encoding="utf8") as f:
        sorted_clusters = [(cluster_id, word) for word, cluster_id in
                           sorted(clusters.iteritems(),
                                  key=operator.itemgetter(1))]
        string_data = "\n".join(
            u"%s\t%s" % (cluster_id, word) for cluster_id, word in
            sorted_clusters)
        f.write(string_data)


def main_compute_world_clusters():
    parser = argparse.ArgumentParser(
        description="Compute word cluster")
    parser.add_argument("input_path", type=unicode)
    parser.add_argument("output_path", type=unicode)
    parser.add_argument("n_clusters", type=int)
    args = parser.parse_args()
    word_vectors = load_word_vectors(args.input_path)
    word_clusters = compute_clusters(word_vectors, args.n_clusters)
    save_word_clusters(word_clusters, args.output_path)
    print("Wrote clusters to %s" % args.output_path)


if __name__ == '__main__':
    main_compute_world_clusters()
