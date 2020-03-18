#!/bin/bash
#####################################
## File name : install_multiagent_particle_envs.sh
## Create date : 2018-11-25 16:03
## Modified date : 2019-11-17 23:19
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

repo_path="../multiagent-particle-envs"

function dlgit_down_repo(){
    down_url="https://github.com/openai/multiagent-particle-envs.git"
    folder=$repo_path
    dlgit_clone_git $down_url $folder
}

function dlgit_rm_repo(){
    rm -rf $repo_path
}

function create_repo(){
    dlfile_check_is_have_dir $repo_path

    if [[ $? -eq 0 ]]; then
        dlgit_down_repo
    else
        $DLLOG_INFO "$1 $repo_path have been created"
#        dlgit_rm_repo
    fi
    #cd $pybase_path
    #pwd
    #bash ./set_up.sh
    #cd -
}

source $env_path/py3env/bin/activate
create_repo
deactivate
