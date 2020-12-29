import argparse
import itertools
import sys
import warnings
from pathlib import Path
from typing import Iterable, Iterator, List, TypeVar

warnings.filterwarnings("ignore", category=RuntimeWarning)
import ffmpeg
import pydub

T = TypeVar("T")

#  Chunk size in ms
CHUNK_SIZE = 100
MIN_GROUP = 10
TRANSITION_CHUNK = 3
# Threshold for what counts as silence in dB
SILENCE_THRESHOLD = -60
# Playback speed for silent section
SILENT_SPEED = 5
# Playback speed for non-silent section
SPEECH_SPEED = 1.5


def main():
    videoFile = Path(args.input).resolve()
    if args.ffmpeg:
        pydub.AudioSegment.converter = args.ffmpeg

    # Construct file names
    audioFile = videoFile.with_name("{}_audio.wav".format(videoFile.stem))
    pbsFile = videoFile.with_name("{}.pbs".format(videoFile.stem))

    # Extract audio
    get_audio(videoFile, audioFile)
    # Open sound file.
    sound = pydub.AudioSegment.from_file(audioFile)

    chunk_silent = [c.dBFS < SILENCE_THRESHOLD for c in chunker(sound, CHUNK_SIZE)]

    normalized = normalize(chunk_silent)

    speed = [SILENT_SPEED if cs else SPEECH_SPEED for cs in normalized]

    pbs_writer(pbsFile, speed)
    print(pbsFile)


def normalize(source):
    normalized = []
    for s, si in itertools.groupby(source):
        sl = list(si)
        if s:
            if len(sl) <= MIN_GROUP:
                normalized += [not bool for bool in sl]
                continue
            else:
                sl[:TRANSITION_CHUNK] = [False] * TRANSITION_CHUNK
                sl[-TRANSITION_CHUNK:] = [False] * TRANSITION_CHUNK
        normalized += sl
    return normalized


def pbs_writer(filename: Path, speed: List[int]):
    f = open(filename, "w")
    f.write("{}\n".format(CHUNK_SIZE))

    f.writelines(
        ["{} {}\n".format(x, len(list(y))) for x, y in itertools.groupby(speed)]
    )

    f.close()


def chunker(seq: Iterable[T], size: int) -> Iterator[List[T]]:
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def get_audio(videofile: Path, outfile: Path):
    cmd = "ffmpeg"
    if args.ffmpeg:
        cmd = args.ffmpeg
    try:
        ffmpeg.input(str(videofile)).audio.output(
            str(outfile), acodec="pcm_s16le", ar=44100, ac=2, nostdin=None
        ).run(quiet=True, overwrite_output=True, cmd=cmd)
    except ffmpeg._run.Error:
        return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pbs file generator")
    parser.add_argument("ffmpeg", help="Path to ffmpeg.exe")
    parser.add_argument("input", help="Input Audio File")
    args = parser.parse_args()
    main()
