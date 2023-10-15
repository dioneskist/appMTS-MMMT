# Implementação de software para comparação do método multimodelo e típico com objetivo de compreender o aprendizado de pessoas com autismo.

- Linha de pesquisa: Análise do comportamento
- Técnica utilizada: multi modelo e típico
- Público alvo: pessoas com autismo

Nota 1. Este software foi construído utilizando com objetivo de ser utilizado em dispositivo móvel sem acesso à internet em ambiente controlado. O app foi produzido com a ferramenta Kivy + python e desenhado para rodar em dispositivo tablet Samsung Tab A 10.1 2016 com resolução de tela 1200x1980


## Como install/rodar no Linux
1. Clonar este repo `git clone git@github.com:dioneskist/appMTS-MMMT.git`
2. Instalar o python: `sudo apt install -y python3`
3. Instalar as dependências: `python -m ensurepip --upgrade;pip3 install -r requirements.txt`
4. Rodar o projeto: `python3 main.py`

Nota 2. Use o python virtual-env para isolar seu ambiente de desenvolvimento

## How to buid and debug android app with Kivy

Install requirements and then run debug

### Requirements

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
      - `ln -s /mnt/d/projetos/tools/platform-tools/adb.exe /home/dione/.buildozer/android/platform/android-sdk/platform-tools/adb`
      - agora só rodar so coamndos:
      1. build `buildozer android debug deploy`
      2. run `buildozer android debug deploy run`
      3. run with debug enabled `buildozer android debug run logcat`