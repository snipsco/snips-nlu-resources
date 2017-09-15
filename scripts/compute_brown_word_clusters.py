# coding=utf-8
from __future__ import unicode_literals

import argparse
import os
import subprocess

from utils import SCRIPTS_PATH

CLUSTER_LIB_PATH = os.path.join(SCRIPTS_PATH, "brown-cluster")
BIN_PATH = os.path.join(CLUSTER_LIB_PATH, "wcluster")


def compute_clusters(input_path, output_path, n_clusters):
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    # ./brown-cluster/wcluster --c 1000 --plen 100 --text weibo_leiden_corpus_tokenized.txt --output_dir my_dir --threads 2
    subprocess.check_call(
        [BIN_PATH, "--text", input_path, "--c", n_clusters],
        cwd=CLUSTER_LIB_PATH)

    print("Saved word clusters to %s" % output_path)


def main_compute_world_clusters():
    parser = argparse.ArgumentParser(
        description="Compute word cluster")
    parser.add_argument("input_path", type=unicode)
    parser.add_argument("output_path", type=unicode)
    parser.add_argument("n_clusters", type=unicode)
    args = vars(parser.parse_args())
    compute_clusters(**args)


if __name__ == '__main__':
    main_compute_world_clusters()
