# Oracle (Work In Progress)

Ever wanted to download youtube video?, ever wanted to have an nice back-end files structure for your favorite youtube videos?. Presenting Oracle project.

This project is using yt-dlp to download youtube videos and then transcribe them with Faster-Whisper. The project is using Python and Conda. The step of the project is to get it to work in Windows and then Linux.

The project is modular and contains three components:

1. Youtube downloader (Go inside youtube folder)
2. Transcriber (Whisper) (Go inside transcribe folder)

The goal is to create an modular project that can be used to download youtube videos and then transcribe them. The project is using Conda to create an virtual environment. The project is using Python 3.9.6.

Each project has its own README.md file and step by step instructions on how to install and use the project.
All of the modules requires Conda to be installed and configured.

The project is using Conda to create an virtual environment for the project. Download and install Conda <https://docs.conda.io/en/latest/miniconda.html>

Good luck and enjoy :D

## Base

Because we are using Conda, its good to install and prepare the environment for the project.

```powershell
conda create -n oracle python=3.11
```

Activate the environment

```powershell
conda activate oracle
```



## What now?

Well, its up to you :D. Start with the project module you desire and follow the instructions. If you have any questions, feel free to ask me. You can also combine them into your pipeline thingy :D.

What I have done is to create an single conda environment and then install all of the modules into that environment. You can also use the project as an template for your own project. Have fun and enjoy.

## Project Description - Youtube

Source: <https://github.com/yt-dlp/yt-dlp>

As the project name implies, its a youtube downloader. The project is using yt-dlp to download youtube videos. The project is using Python and Conda. The step of the project is to get it to work in Windows and then Linux.

## Project Description - Transcriber (Whisper)

Primary Source: <https://github.com/Purfview/whisper-standalone-win>

Secondary Source: <https://github.com/guillaumekln/faster-whisper>

The project is using Faster-Whisper to transcribe the downloaded youtube videos. The project is using Python and Conda. The step of the project is to get it to work in Windows and then Linux.

## Project Description - FFmpeg

Source: <https://github.com/FFmpeg/FFmpeg>

The project is using FFmpeg to convert the downloaded youtube videos to different formats, my project just converts them into mp3 for later transcription.

## Thanks

Many thanks for the open source community for making this project possible. Also thanks  Tay, Chad and Data for the support during the development of this project.

## TODO

Future development of the project.

- [X] Basic Modules (youtube, transcribe, ffmpeg)
- [ ] Implement DB (MongoDB)
  - [ ] Research, Education, Development
  - [ ] Implement data ingestion
- [ ] Vector Storage
  - [ ] Research, Education, Development
  - [ ] Implement data ingestion
- [ ] Implement GUI
  - [ ] Research, Education, Development
  - [ ] Implement solution
