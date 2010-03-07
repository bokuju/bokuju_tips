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
smtpd_conf="/usr/lib/sasl2/smtpd.conf"
dovecot_conf="/etc/dovecot.conf"
backup_files=`cat<<_EOT_
${main_cf}
${master_cf}
${smtpd_conf}
${dovecot_conf}
_EOT_`

###
# Functions
#

# main.cf
# TODO:改行した設定も扱えるようにする
function check_main_cf(){
    # 設定があるかチェックする
    local _key=$1
    local _ret=0

    check_key_eq_value "${main_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function get_main_cf(){
    # 設定を取得する
    local _key=$1
    local _ret=0

    get_key_eq_value "${main_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function set_main_cf(){
    # 設定を追加／編集する
    local _key=$1
    local _value=$2
    local _ret=0

    set_key_eq_value "${main_cf}" "${_key}" "${_value}"
    _ret=$?

    return ${_ret}
}

# /usr/lib/sasl2/smtpd.conf
function check_smtpd_conf(){
    # 設定があるかチェックする
    local _key=$1
    local _ret=0

    check_key_col_value "${smtpd_conf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function get_smtpd_conf(){
    # 設定を取得する
    local _key=$1
    local _ret=0

    get_key_col_value "${smtpd_conf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function set_smtpd_conf(){
    # 設定を追加／編集する
    local _key=$1
    local _value=$2
    local _ret=0

    set_key_col_value "${smtpd_conf}" "${_key}" "${_value}"
    _ret=$?

    return ${_ret}
}

# master.cf
# TODO:未作成
function check_master_cf(){
    # 設定があるかチェックする
    local _key=$1
    local _ret=0

    get_key_eq_value "${master_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function get_master_cf(){
    # 設定を取得する
    local _key=$1
    local _ret=0

    get_key_eq_value "${master_cf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function set_master_cf(){
    # 設定を追加／編集する
    local _key=$1
    local _value=$2
    local _ret=0

    set_key_eq_value "${master_cf}" "${_key}" "${_value}"
    _ret=$?

    return ${_ret}
}

# dovecot.conf
function check_dovecot_conf(){
    # 設定があるかチェックする
    local _key=$1
    local _ret=0

    check_key_eq_value "${dovecot_conf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function get_devecot_conf(){
    # 設定を取得する
    local _key=$1
    local _ret=0

    get_key_eq_value "${dovecot_conf}" "${_key}"
    _ret=$?

    return ${_ret}
}

function set_dovecot_conf(){
    # 設定を追加／編集する
    local _key=$1
    local _value=$2
    local _ret=0

    set_key_eq_value "${dovecot_conf}" "${_key}" "${_value}"
    _ret=$?

    return ${_ret}
}
