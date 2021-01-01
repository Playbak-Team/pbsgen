# pbsgen .pbs file generator

## .pbs file format 
.pbs file is a plain-text file formate that describes video playback speed.

File Format:
```
CHUNK_SIZE(ms)
Speed #_of_Chunks
Speed #_of_Chunks
Speed #_of_Chunks
.
.
.
Speed #_of_Chunks
```

Example:
```
500
5 4
1.5 7
5 2
1.5 8
5 1
1.5 4
5 1
1.5 2
5 2
```
This file uses chunk size 500ms. 

The first 4 chunks (0:00-0:02) are played at 5x speed.

Then Next 7 chunks (0:02:000-0:05:500) are played back at 1.5x speed. etc...

## CLI Usage
```
usage: pbsgen.exe [-h] [--version] [--chunk_size CHUNK_SIZE] [--silence_threshold SILENCE_THRESHOLD] [--silent_speed SILENT_SPEED] [--speech_speed SPEECH_SPEED] ffmpeg input

pbs file generator

positional arguments:
  ffmpeg                Path to ffmpeg.exe
  input                 Input Video File

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --chunk_size CHUNK_SIZE
                        Chunk size in ms (default: 100)
  --silence_threshold SILENCE_THRESHOLD
                        Threshold for what counts as silence in dB (default: -60)
  --silent_speed SILENT_SPEED
                        Playback speed for silent section (default: 3)
  --speech_speed SPEECH_SPEED
                        Playback speed for non-silent section (default: 1.5)
```
