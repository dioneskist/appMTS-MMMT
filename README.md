## How to debug android app
# Implementation of software to compare the multi-model and typical method with the aim of understanding the learning of people with autism.

- Line of research: Behavior analysis
- Technique used: multi model and typical method
- Target audience: people with autism

Note 1. This software was built with the aim of being used on a mobile device without internet access in a controlled environment. The app was produced with the Kivy + python tool and designed to run on a Samsung Tab A 10.1 2016 tablet device with 1200x1920 screen resolution


## How to install/run on Linux (WSL)
1. Clone this repo `git clone git@github.com:dioneskist/appMTS-MMMT.git`
2. Install python and pip and so dependencies: `sudo apt update; sudo apt install -y python3 python3-pip libmtdev-dev libgl1-mesa-glx xclip`
3. Install virtualenv `sudo apt install python3-venv; python3 -m venv .venv; source .venv/bin/activate` (Optional)
4. Install the dependencies: `pip3 install -r requirements.txt`
4. Run the project: `python3 main.py`

Note 2. Use python virtual-env to isolate your development environment

## How to build and debug Kivy app and Android

Install requirements and then run debug

### Requirements

- buildozer - [Instalation](https://buildozer.readthedocs.io/en/latest/installation.html)
- adb
- java


### Steps to install adb:
1. Download JDK and add JAVA_HOME environment
2. Download https://developer.android.com/tools/releases/platform-tools
3. Run adb devices to get devide ID
4. Finally, run adb to get logs from device `.\adb.exe logcat -v threadtime 520378ff4c18b3df > D:\project\app\android-debug.log`

### Steps to run kivy built to android
1. `source .venv/bin/activate`
2. `buildozer android debug`
3. Deploy app to device `buildozer android run debug`

Tips for you Linux and Pycham lover running Linux on WSL:

1. Create a separate virtualenv environment on Windows file system to use with Pycharm and another one to use in linux system
  - Linux:
    - `python3 -m venv .venv`
    `source .venv/bin/activate`
    - `python -m pip install -r requirements.txt`

  - Windows (PowerShell):
    - `py -m venv env-win`
    - `.\env-win\Scripts\activate`
    - `python.exe -m pip install -r requirements.txt`

2. Deploy android app from WSL to device connected on Windows:
  - Necessário que o comando adb executado seja o executável windows e não o adb do linux (ver [aqui](https://stackoverflow.com/questions/60166965/adb-device-list-empty-using-wsl2))
    - Crie um link para alterar o adb chamado para o adb do windows:
      - `ln -s /mnt/e/projetos/tools/platform-tools/adb.exe /home/dione/.buildozer/android/platform/android-sdk/platform-tools/adb`
      - agora só rodar so coamndos:
      1. build `buildozer android debug deploy`
      2. build, deploy and run `buildozer android debug deploy run`
      3. run with debug enabled `buildozer android debug run logcat`