# YAASA
YAASA (Yet Another APK Static Analyzer) is a framework for having fun with analyzing APKs.   
The project is using the tools below and is built on Django framework:
- [APKTool](https://ibotpeaches.github.io/Apktool/): A tool for reverse engineering Android apk files
- [AxmlParserPY](https://github.com/kzjeef/AxmlParserPY): Python AxmlParser
- [PlagueScanner](https://github.com/PlagueScanner/PlagueScanner): Open source multiple AV scanner framework

You can add new functions in ```analyze/libs/threads.py```.

## Use
Usage of the app is very easy. You can start the YAASA with ```python manage.py runserver``` and open ```127.0.0.1:8000``` on your browser. After, you can upload your apk file and let the framework to start analysis process in background.

## Anti-Virus
For take power of Anti-Viruses, you must run some virtual machines with Anti-Virus installed on them. For more information you can see [PlagueScanner](https://github.com/PlagueScanner/PlagueScanner) page. Some agents need to be modified to provide best result of scanning. We modified BitDefender agent for that purpose.

## Install
You can run these commands to install the framework:
```
git clone https://github.com/mohammadnassiri/YAASA.git
cd YAASA
pip3 install -r requirements.txt
```

## Config
```.env ``` file must be configured before using the YAASA framework. If you use a MySQL database, connection variables should be set in this file. Also set a secret_key which is used by django itself.


## Paper
Paper published [here](http://apa3.apaconf.ir/) (persian).   
For more information please [contact me](https://mnassiri.ir).