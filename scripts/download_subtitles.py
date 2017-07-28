# coding=utf-8
from __future__ import unicode_literals

import argparse
import io
import re

from babelfish import Language
from subliminal import Video, download_best_subtitles

HTML_RE = re.compile(r"\</?[a-z]\>")
TIME_RE = re.compile(r"[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}")
DIGIT_RE = re.compile(r"(?<=\s)[0-9]+(?=\s)")


def format_subtitle(text):
    # Remove HTML
    text = HTML_RE.sub("", text)
    # Remove time
    text = TIME_RE.sub("", text)
    # Remove arrows
    text = text.replace("-->", "")
    # Remove digits
    text = DIGIT_RE.sub("", text)
    return text


def download_series_subtitles(series_name, language,
                              possible_encodings=["utf8"]):
    subtitles = []
    episode = 0
    season = 1
    finished_serie = False
    already_raised_exception = False
    current_encoding = possible_encodings[0]
    while not finished_serie:
        while True:
            episode += 1
            try:
                video = Video.fromname(
                    "%s season %i episode %i" % (series_name, season, episode))
                best_subtitles = download_best_subtitles(
                    {video}, {Language(language)})
                best_subtitle = best_subtitles[video][0]

                try:
                    episode_subtitles = best_subtitle.content.decode(
                        current_encoding)
                except UnicodeDecodeError:
                    for i, encoding in enumerate(possible_encodings):
                        try:
                            episode_subtitles = best_subtitle.content.decode(
                                encoding)
                            current_encoding = encoding
                        except UnicodeDecodeError:
                            if i == len(possible_encodings) - 1:
                                raise ValueError(
                                    "Could not find a valid encoding in %s" %
                                    possible_encodings)
                episode_subtitles = format_subtitle(episode_subtitles)
                episode_subtitles = [m for m in episode_subtitles.split("\n")
                                     if len(m.strip()) > 0]
                subtitles += episode_subtitles
                already_raised_exception = False
                print(
                    "Downloaded subtitles from: {series} {season} episode "
                    "{episode}".format(
                        series=series_name,
                        season=season,
                        episode=episode)
                )
            except IndexError:
                if already_raised_exception:
                    finished_serie = True
                    break
                already_raised_exception = True
                print("End of season %s\n" % season)
                episode = 0
                season += 1
                break

        if finished_serie:
            break

    return subtitles


def main_download():
    parser = argparse.ArgumentParser(
        description="Download all subtitle from a serie into a single text "
                    "file")
    parser.add_argument("series_name", type=str, help="Name of the series")
    parser.add_argument("language", type=str, help="Babelfish Language")
    parser.add_argument("output_path",
                        type=str,
                        help="Path to the file where the subtitle will be "
                             "save")
    parser.add_argument("possible_encodings", type=str, nargs="+",
                        help="Encoding of the subtitles")
    args = vars(parser.parse_args())
    output_path = args.pop("output_path")
    subtitles = download_series_subtitles(**args)
    with io.open(output_path, "w", encoding="utf8") as f:
        f.write("\n".join(subtitles))
    print("Saved subtitles to %s" % output_path)


if __name__ == '__main__':
    main_download()
