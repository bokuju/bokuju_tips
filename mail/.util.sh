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

function make_Maildir(){
    # Maildirを作成する
    # TODO 返り値の処理
    local _ret=0

    if [ ! -d "/etc/skel/Maildir" ]; then
        mkdir -p /etc/skel/Maildir/{new,cur,tmp}
        chmod -R 700 /etc/skel/Maildir
    fi

    for _user in `ls -1 /home`
    do
        if [ ! -d "/home/${_user}/Maildir" ]; then
            mkdir "/home/${_user}/Maildir"
        fi
    done

    if [ ! -d "/root/Maildir" ]; then
        mkdir "/root/Maildir"
    fi

    return ${_ret}
}

function check_auto_start(){
    # chkconfigがONかチェックする
    local _ret=0
    local _daemon=$1

    chkconfig --list ${_daemon} | grep -q "on"
    _ret=$?

    return ${_ret}
}

function set_auto_start(){
    # chkconfigをON/OFFする
    local _ret=0
    local _daemon=$1
    local _action=$2

    check_auto_start ${_daemon}
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        chkconfig ${_daemon} ${_action} 
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "${_daemon} auto start ${_action} ... ok"
        else
            error "${_daemon} auto start ${_action} ... failed"
        fi
    fi

    return ${_ret}
}

function check_daemon(){
    # デーモンが起動しているかチェックする
    local _ret=0
    local _daemon=$1

    if [ -f /etc/init.d/${_daemon} ]; then
        /etc/init.d/${_daemon} status > /dev/null
        _ret=$?
    else
        error "Error: not found ${_daemon} daemon"
        _ret=1
    fi

    return ${_ret}
}

function start_daemon(){
    # デーモンを起動する
    local _ret=0
    local _daemon=$1

    check_daemon ${_daemon}
    _ret=$?
    if [ ${_ret} -ne 0 ]; then
        /etc/init.d/${_daemon} start > /dev/null
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "${_daemon} start ... ok"
        else
            error "${_daemon} start ... failed"
        fi
    fi

    return ${_ret}
}

function stop_daemon(){
    # デーモンを停止する
    local _ret=0
    local _daemon=$1

    check_daemon ${_daemon}
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        /etc/init.d/${_daemon} stop > /dev/null
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "${_daemon} stop ... ok"
        else
            error "${_daemon} stop ... failed"
        fi
    fi

    return ${_ret}
}

function check_mta_is_postfix(){
    # TODO:sendmailにも対応
    LANG=C alternatives --display mta | grep 'link currently points to' | grep -q "postfix"
    _ret=$?

    return ${_ret}
}

function set_mta_is_postfix(){
    # TODO:sendmailにも対応

    check_mta_is_postfix
    _ret=$?
    if [ ${_ret} -ne 0 ]; then
        echo "2" | alternatives --config mta
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "set mta is postfix ... ok"
        else
            error "set mta is postfix ... failed"
        fi
    fi
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

# key:value
function check_key_col_value(){
    # 設定ファイルに設定があるかチェックする
    local _file=$1
    local _key=$2
    egrep -q "^[ \t]*${_key}[ \t]*:[ \t]*.*" "${_file}"
    _ret=$?

    return ${_ret}
}

function get_key_col_value(){
    # 設定ファイルに設定を取得する
    local _file=$1
    local _key=$2
    local _ret=0

    check_key_col_value "${_file}" ${_key}""
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        egrep "^[ \t]*${_key}[ \t]*:[ \t]*.*" "${_file}" | sed -e "s/^[ \t]*${_key}[ \t]*:[ \t]*\(.*\)/\1/;"
        _ret=$?
    fi

    return ${_ret}
}

function set_key_col_value(){
    # 設定ファイルに設定を追加／編集する
    # TODO:シェルで使用される文字のエスケープ
    local _file=$1
    local _key=$2
    local _value=$3
    local _ret=0

    check_key_col_value "${_file}" ${_key}""
    _ret=$?
    if [ ${_ret} -eq 0 ]; then
        #edit
        sed -i -e "s/^[ \t]*${_key}[ \t]*:[ \t]*.*/${_key}:${_value}/;" "${_file}"
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "setting ${_file}, edit (${_key}:${_value}) ... ok"
        else
            error "setting ${_file}, edit (${_key}:${_value}) ... failed, exit=(${_ret})"
        fi
    else
        #new
        echo "${_key}:${_value}" >> "${_file}"
        _ret=$?
        if [ ${_ret} -eq 0 ]; then
            log "setting ${_file}, add (${_key}:${_value}) ... ok"
        else
            error "setting ${_file}, add (${_key}:${_value}) ... failed, exit=(${_ret})"
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
