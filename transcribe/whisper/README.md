# Module : Transcribe (Whisper) Windows Edition

We will use <https://github.com/Purfview/whisper-standalone-win> for Windows. The project is using Python and Conda. In the future I will support Linux.

This guide will start with the assumption that you have installed Conda and configured it. If you have not, please follow the guide in the Base module. We will install conda environment and then install the required packages. After that we will install python packages.

If you are using GPU you need to have the GPU drivers installed. You also need to install CUDA and CUDNN. I will cover that in step by step, this guide supports right now this guide supports NVIDIA GPU with CUDA.

## Step 1 - NVIDIA GPU

This step will cover how to get your GPU to work with CUDA and CUDNN. If you are using CPU, you can skip this step.

### Step 1.1 - NVIDIA GPU - CUDA

Start an terminal and run the following command:

```powershell
nvidia-smi
```

You are looking for the version number of your GPU. In my case its CUDA Version: 12.2. You can also check the version number in the NVIDIA Control Panel.

```powershell
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.98                 Driver Version: 535.98       CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                     TCC/WDDM  | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 4080      WDDM  | 00000000:01:00.0  On |                  N/A |
| 31%   39C    P5              39W / 320W |  14463MiB / 16376MiB |     40%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
```

Based on that we need to download the correct version of CUDA. You can find the correct version here: <https://developer.nvidia.com/cuda-toolkit-archive>. I will select CUDA Toolkit 12.1.1:
<https://developer.nvidia.com/cuda-12-1-1-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local>

Download the version you need and install it :D.

### Step 1.2 - NVIDIA GPU - CUDNN

Because we are using Pytorch we need to install CUDNN. You can find the correct version here: <https://developer.nvidia.com/rdp/cudnn-archive>. I will select cuDNN Library for Local Installer for Windows (Zip). This requires you to have an account. You can create one for free.

Unzip the folder, inside the Bin folder copy all the files to whisper root directory. In my case its \Oracle\transcribe\whisper.

This is how it will look like:

```powershell
# Directory: C:\Oracle\transcribe\whisper

├── Oracle
│ ├── transcribe
│ │ ├── whisper
│ │ │ ├── cudnn_adv_infer64_8
│ │ │ ├── cudnn_adv_train64_8.dll
│ │ │ ├── cudnn_cnn_infer64_8.dll
│ │ │ ├── cudnn_cnn_train64_8.dll
│ │ │ ├── cudnn_ops_infer64_8.dll
│ │ │ ├── cudnn_cnn_infer64_8.dll
│ │ │ ├── cudnn_ops_train64_8.dll
│ │ │ ├── cudnn64_8.dll
```

### Step 1.3 - NVIDIA GPU - Cuda Toolkit

We installed Cuda Toolkit and because the whisper-standalone-win needs the cublas64_11.dll, cublasLt64_11.dll in the same directory as where the bin file is "whisper-faster.exe". We need to copy the two files from Cuda toolkit to the whisper root directory. In my case its \Oracle\transcribe\whisper.

Files are being copied from:

```powershell
# Copy from 
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin
cublas64_12.dll
cublasLt64_12.dll
```

```powershell
# Copy to 
# Directory: C:\Oracle\transcribe\whisper

├── Oracle
│ ├── transcribe
│ │ ├── whisper
│ │ │ ├── cublas64_12.dll
│ │ │ ├── cublasLt64_12.dll
```

## Step 2 - Conda Environment

We will use Pytorch and we need to install it. We will use Conda to install it. We will use out base environment and install Pytorch. We will also install the required packages.

Based on your Cuda toolkit version, lets get the correct command for Pytorch. You can find the correct version here: <https://pytorch.org/>. I will select Pytorch Preview (Nightly).

Please activate the conda environment you want to install Pytorch in. In my case its oracle.

```powershell
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch-nightly -c nvidia
```

## Step 3 - Python Packages

```powershell
pip install -r .\transcribe\whisper\requirements.txt
```

## Step 4 - Edit the config file

Based on your onw preference I recommend edit the settings.yaml file for your environment. You can find the file here: \Oracle\transcribe\whisper\settings.yaml. The settings.yaml are now tune  to work with the Youtube downloader module. You need to edit the settings.yaml file to match your environment.

The to get your started edit the Basic configuration. The configuration has comments and more information about the configuration.

```yaml
######################### BASIC CONFIGURATION #########################
# device to use (default: cuda) or cpu
DEVICE: "cuda"
# Set the language
LANGUAGE: 'English'
# https://github.com/guillaumekln/faster-whisper#large-v2-model-on-gpu
# https://github.com/guillaumekln/faster-whisper#small-model-on-cpu
# https://huggingface.co/openai/whisper-large
# whisper-small
# THis flags tells you where you can find the models large-v2
# ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large-v1', 'large-v2']
MODEL: "large-v2"
# Where the models are stored
MODEL_DIR: "models"
# This flag sets the maximum width for each line of the 
# transcription to 100 characters. If a line exceeds this width, 
# the text will wrap to the next line.
MAX_LINE_WIDTH: 100
# Output Print Debug
DEBUG: false
# No timestamp printed in output txt file
WORD_TIMESTAMPS: true
######################### BASIC CONFIGURATION #########################
```

## Step 5 - Run the script

```powershell
python .\transcribe\whisper\main.py
```
