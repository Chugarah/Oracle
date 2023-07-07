# Introducing Oracle: A Modular Project for Downloading and Transcribing YouTube Videos

Oracle is a project designed to provide a convenient solution for downloading and transcribing YouTube videos. It utilizes the yt-dlp tool for video downloads and Faster-Whisper for transcription. The project is developed using Python and Conda, with the objective of ensuring compatibility with both Windows and Linux operating systems.

The project comprises three distinct components:

YouTube Downloader: Found inside the "youtube" folder, this module facilitates easy downloading of YouTube videos.

Transcriber (Whisper): Located in the "transcribe" folder, this module offers seamless transcription functionality using Faster-Whisper.

The primary goal of Oracle is to create a modular framework that streamlines the process of downloading YouTube videos and transcribing their contents. It leverages Conda to create a virtual environment and relies on Python 3.9.6 for its implementation.

Each component of the project is accompanied by a detailed README.md file, providing step-by-step instructions for installation and usage. It is important to note that all modules require the prior installation and configuration of Conda.

To begin using Oracle, please ensure Conda is installed and configured on your system. You can download and install Conda from this link: Conda Installation Guide

Wishing you the best of luck and a delightful experience with Oracle!

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
