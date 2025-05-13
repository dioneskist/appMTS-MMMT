# Implementação de software para comparação do método multimodelo e típico com objetivo de compreender o aprendizado de pessoas com autismo.

- Linha de pesquisa: Análise do comportamento
- Técnica utilizada: multi modelo e típico
- Público alvo: pessoas com autismo

Nota 1. Este software foi construído utilizando com objetivo de ser utilizado em dispositivo móvel sem acesso à internet em ambiente controlado. O app foi produzido com a ferramenta Kivy + python e desenhado para rodar em dispositivo tablet Samsung Tab A 10.1 2016 com resolução de tela 1200x1920


## Como install/rodar no Linux (WSL)
1. Clonar este repo `git clone https://github.com/dioneskist/pareamentos.git`
2. Instalar o python, pip e dependencies: `sudo apt update; sudo apt install -y python3 python3-pip libmtdev-dev libgl1-mesa-glx xclip`
3. Instalar virtualenv `sudo apt install python3-venv; python3 -m venv .venv; source .venv/bin/activate` (Opcional)
4. Instalar as dependências:  `cd pareamentos; pip3 install -r requirements.txt`
5. Rodar o projeto: `python3 main.py`

Nota 2. Use o python virtual-env para isolar seu ambiente de desenvolvimento

## Como construir e debugar aplicativos Kivy no Android

Instale os requisitos e execute a depuração

###Requisitos

- adb
- java

### Etapas para instalar o adb:
1. Baixe o JDK e adicione o ambiente JAVA_HOME
2. Baixe https://developer.android.com/tools/releases/platform-tools
3. Execute dispositivos adb para obter o devido ID
4. Por fim, execute adb para obter logs do dispositivo `.\adb.exe logcat -v threadtime 520378ff4c18b3df > D:\project\app\android-debug.log`

### Etapas para executar o Kivy desenvolvido para Android
1. `source .venv/bin/ativar`
2. `buildozer android debug`
3. Implante o aplicativo no dispositivo `buildozer android run debug`

Dicas para você amante de Linux e Pycham rodando Linux no WSL:

1. Crie um ambiente virtualenv separado no sistema de arquivos Windows para usar com Pycharm e outro para usar no sistema Linux
    -Linux:
      - `python3 -m venv.venv`
      - `source .venv/bin/ativar`
      - `python -m pip install -r requisitos.txt`

    -Windows (PowerShell):
      - `py -m venv env-win`
      - `.\env-win\Scripts\activate`
      - `python.exe -m pip install -r requirements.txt`
2. Implante o aplicativo Android do WSL no dispositivo conectado no Windows:
    - O comando adb executado deve ser o executável do Windows e não o adb do Linux (veja [aqui](https://stackoverflow.com/questions/60166965/adb-device-list-empty-using-wsl2))
    - Crie um link para alterar o adb chamado para o adb do windows:
    - `ln -s /mnt/d/projetos/tools/platform-tools/adb.exe /home/dione/.buildozer/android/platform/android-sdk/platform-tools/adb`
    - agora é só executar os seguintes comandos:
      1. construir `buildozer android debug deploy`
      2. execute `buildozer android debug deploy run`
      3. execute com depuração habilitada `buildozer android debug run logcat`
