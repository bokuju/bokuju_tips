#!/bin/bash

###
# Settings
#
main_cf="/etc/postfix/main.cf"
master_cf="/etc/postfix/master.cf"
backup_files=`cat<<_EOT_
${main_cf}
${master_cf}
_EOT_`
BACKUP_SUFFIX=".bak"

###
# Functions
#
function get_domainname(){
    local _hostname=$1  
    echo "${_hostname}" | cut -d. -f2-
    return 0
}

function set_key_eq_value() {
    local _file=$1
    local _key=$2
    local _value=$3
    local _ret=0
    egrep -q "^[ \t]*${_key}[ \t]*=[ \t]*.*" "${_file}"
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        #edit
        sed -i -e "s/^[ \t]*${_key}[ \t]*=[ \t]*.*/${_key} = ${_value}/;" "${_file}"
        _ret=$?
    else
        #new
        echo "${_key} = ${_value}" >> "${_file}"
        _ret=$?
    fi
    return ${_ret}
}

function get_key_eq_value(){
    local _file=$1
    local _key=$2
    local _ret=0

    egrep -q "^[ \t]*${_key}[ \t]*=[ \t]*.*" "${_file}"
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        egrep "^[ \t]*${_key}[ \t]*=[ \t]*.*" "${_file}" | sed -e "s/^[ \t]*${_key}[ \t]*=[ \t]*\(.*\)/\1/;"
        _ret=$?
    fi

    return ${_ret}
}


function backup(){
    local _file="$@"
    local _ret=0

    for _f in ${_file}
    do
        cp -fp ${_f}{,${BACKUP_SUFFIX}}
        _ret=$?
        if [ ${_ret} -ne 0 ]; then
            echo "${_f} backup is failed." > /dev/stderr
            break
        fi
    done
    return ${_ret}
}

function check_backup(){
    local _file="$@"
    local _ret=0

    for _f in ${_file}
    do
        if [ ! -f "${_f}${BACKUP_SUFFIX}" ]; then
            _ret=1
        fi
    done
    return ${_ret}
}

function remove_backup(){
    local _file="$@"
    local _ret=0

    for _f in ${_file}
    do
        if [ -f "${_f}${BACKUP_SUFFIX}" ]; then
            rm -f "${_f}${BACKUP_SUFFIX}"
        fi
    done
    return ${_ret}
}
function restore(){
    local _file="$@"
    local _ret=0

    for _f in "${_file}"
    do
        mv -f ${_f}{${BACKUP_SUFFIX},}
        _ret=$?
        if [ ${_ret} -ne 0]; then
            echo "${_f} restore is failed." > /dev/stderr
            break
        fi
    done
    return ${_ret}
}
