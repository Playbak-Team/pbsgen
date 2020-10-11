# pbsgen .pbs file generator
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
