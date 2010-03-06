#!/bin/bash

###
# 汎用関数
#

###
# Settings
#
BACKUP_SUFFIX=".bak"

###
# Functions
#

# Utils
function get_domainname(){
    # ドメインネームを取得する
    local _hostname=$1  
    echo "${_hostname}" | cut -d. -f2-
    return 0
}

function log(){
    # ログを出力する
    local _msg=$1
    local _log=/dev/stdout
    local _ret=0
    echo "${_msg}" > ${_log}
    return ${_ret}
}

function error(){
    # エラーを出力する
    local _msg=$1
    local _error=/dev/stderr
    local _ret=0
    echo "${_msg}" > ${_error}
    return ${_ret}
}

function escape(){
    # シェルで使用される記号のエスケープをする
    # TODO:未作成
    local _value=$1
    local _ret=0
    return ${_ret}
}

# key=value
function check_key_eq_value(){
    # 設定ファイルに設定があるかチェックする
    local _file=$1
    local _key=$2
    egrep -q "^[ \t]*${_key}[ \t]*=[ \t]*.*" "${_file}"
    _ret=$?

    return ${_ret}
}

function get_key_eq_value(){
    # 設定ファイルに設定を取得する
    local _file=$1
    local _key=$2
    local _ret=0

    check_key_eq_value "${_file}" ${_key}""
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        egrep "^[ \t]*${_key}[ \t]*=[ \t]*.*" "${_file}" | sed -e "s/^[ \t]*${_key}[ \t]*=[ \t]*\(.*\)/\1/;"
        _ret=$?
    fi

    return ${_ret}
}

function set_key_eq_value(){
    # 設定ファイルに設定を追加／編集する
    # TODO:シェルで使用される文字のエスケープ
    local _file=$1
    local _key=$2
    local _value=$3
    local _ret=0

    check_key_eq_value "${_file}" ${_key}""
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        #edit
        sed -i -e "s/^[ \t]*${_key}[ \t]*=[ \t]*.*/${_key} = ${_value}/;" "${_file}"
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "setting ${_file}, edit (${_key} = ${_value}) ... ok"
        else
            error "setting ${_file}, edit (${_key} = ${_value}) ... failed, exit=(${_ret})"
        fi
    else
        #new
        echo "${_key} = ${_value}" >> "${_file}"
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "setting ${_file}, add (${_key} = ${_value}) ... ok"
        else
            error "setting ${_file}, add (${_key} = ${_value}) ... failed, exit=(${_ret})"
        fi
    fi
    return ${_ret}
}

# backup/restore
function backup(){
    # ファイルのバックアップをする
    local _file="$@"
    local _ret=0

    for _f in ${_file}
    do
        cp -fp ${_f}{,${BACKUP_SUFFIX}}
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "create backup ${_f} ... ok"
        else
            error "create backup ${_f} ... failed, exit=(${_ret})"
            break
        fi
    done
    return ${_ret}
}

function check_backup(){
    # バックアップがあるかチェックする
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
    # バックアップを削除する
    local _file="$@"
    local _ret=0

    for _f in ${_file}
    do
        if [ -f "${_f}${BACKUP_SUFFIX}" ]; then
            rm -f "${_f}${BACKUP_SUFFIX}"
            _ret=$?
            if [ ${_ret} -eq 0 ]; then
                log "remove backup ${_f} ... ok"
            else
                error "remove backup ${_f} ... failed, exit=(${_ret})"
                break
            fi
        fi
    done
    return ${_ret}
}

function restore(){
    # バックアップから設定を切り戻す
    local _file="$@"
    local _ret=0

    for _f in "${_file}"
    do
        mv -f ${_f}{${BACKUP_SUFFIX},}
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "restore ${_f} ... ok"
        else
            error "resotre ${_f} ... failed, exit=(${_ret})"
            break
        fi
    done
    return ${_ret}
}
