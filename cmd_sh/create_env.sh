#!/bin/bash
#####################################
## File name : create_env.sh
## Create date : 2018-11-25 15:54
## Modified date : 2019-11-17 23:27
## Author : DARREN
## Describe : not set
## Email : lzygzh@126.com
####################################

realpath=$(readlink -f "$0")
export basedir=$(dirname "$realpath")
export filename=$(basename "$realpath")
export PATH=$PATH:$basedir/dlbase
export PATH=$PATH:$basedir/dlproc
#base sh file
. dlbase.sh
#function sh file
. etc.sh
#asumming installed virtualenv　

rm -rf $env_path
mkdir $env_path
cd $env_path

#   virtualenv -p /usr/bin/python2 py2env
#   source $env_path/py2env/bin/activate
#   pip install Pillow
#   #pip install tornado
#   #pip install mysqlclient
#   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade numpy 
#   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade matplotlib==2.2.2
#   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade torch
#   #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade torchvision
#   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade nltk
#   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade spacy
#   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade torchtext
#   #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade scikit-image
#   #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pandas
#   #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade ipython

#   deactivate

virtualenv -p /usr/bin/python3 py3env
source $env_path/py3env/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade numpy
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple torch

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jupyter
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gym[all]
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade grpcio
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade grpcio-tools
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade websockets
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade websocket
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade websocket_client
deactivate
