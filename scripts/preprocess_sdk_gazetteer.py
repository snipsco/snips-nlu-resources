import argparse
import io
import json
import os

from utils import ROOT_PATH


def process(input_path, output_path):
    with io.open(os.path.join(ROOT_PATH, input_path), encoding="utf8") as f:
        data = json.load(f)

    with io.open(os.path.join(ROOT_PATH, output_path), "w",
                 encoding="utf8") as f:
        f.write("\n".join(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = vars(parser.parse_args())
    process(**args)
