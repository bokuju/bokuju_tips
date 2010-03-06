#!/bin/bash

###
# Postfix用関数
#

###
# Including
#
if [ -f $(pwd $0)/.util.sh ]; then
    source $(pwd $0)/.util.sh
fi

###
# Settings
#
main_cf="/etc/postfix/main.cf"
master_cf="/etc/postfix/master.cf"
backup_files=`cat<<_EOT_
${main_cf}
${master_cf}
_EOT_`

###
# Functions
#

# main.cf
# TODO:改行した設定も扱えるようにする
function check_main_cf(){
    # main.cfに設定があるかチェックする
    local _key=$1
    local _ret=0

    check_key_eq_value "${main_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function get_main_cf(){
    # main.cfの設定を取得する
    local _key=$1
    local _ret=0

    get_key_eq_value "${main_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function set_main_cf(){
    # main.cfの設定を追加／編集する
    local _key=$1
    local _value=$2
    local _ret=0

    set_key_eq_value "${main_cf}" "${_key}" "${_value}"
    _ret=$?

    return ${_ret}
}

# master.cf
# TODO:未作成
function check_master_cf(){
    local _key=$1
    local _ret=0

    get_key_eq_value "${master_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function get_master_cf(){
    local _key=$1
    local _ret=0

    get_key_eq_value "${master_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function set_master_cf(){
    local _key=$1
    local _value=$2
    local _ret=0

    set_key_eq_value "${master_cf}" "${_key}" "${_value}"
    _ret=$?

    return ${_ret}
}
