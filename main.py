import itertools
import sys
from pathlib import Path
from typing import Iterable, Iterator, List, TypeVar

import ffmpeg
import pydub

T = TypeVar("T")

CHUNK_SIZE = 500
SILENCE_THRESHOLD = -40
SILENT_SPEED = 5
SPEECH_SPEED = 1.5


def main(videoFile: Path):
    audioFile = videoFile.with_name("{}_audio.aac".format(videoFile.stem))
    get_audio(videoFile, audioFile)
    sound = pydub.AudioSegment.from_file(audioFile)
    chunk_silent = (
        SILENT_SPEED if c.dBFS < SILENCE_THRESHOLD else SPEECH_SPEED
        for c in chunker(sound, CHUNK_SIZE)
    )
    pbsFile = videoFile.with_name("{}.pbs".format(videoFile.stem))

    pbs_writer(pbsFile, chunk_silent)


def pbs_writer(filename: Path, speed: List[int]):
    f = open(filename, "w")
    f.write("{}\n".format(CHUNK_SIZE))
    f.writelines(["{} {}\n".format(x, len(list(y))) for x, y in itertools.groupby(speed)])
    f.close()



def chunker(seq: Iterable[T], size: int) -> Iterator[List[T]]:
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def get_audio(videofile: Path, outfile: Path):
    try:
        ffmpeg.input(str(videofile)).audio.output(
            str(outfile), acodec="copy", nostdin=None
        ).run(quiet=True, overwrite_output=True)
    except ffmpeg._run.Error:
        return False
    return True


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
