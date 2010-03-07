#!/bin/bash

###
# メールの初期設定をするスクリプト
#

###
# Including
#
if [ -f $(pwd $0)/.mail_util.sh ]; then
    source $(pwd $0)/.mail_util.sh
fi

###
# Settings
#
ret=0
domainname="$(get_domainname $(hostname))"

###
# Main
#
# TODO: バックアップ、基本設定、SMTP−Auth、受信メールサイズ制限を別のプログラムにする
# TODO: 実行できるユーザーのチェック rootだけ
# TODO: 返り値の処理
backup ${backup_files}

# postfix基本設定
set_main_cf 'myhostname' "mail.${domainname}"
new_myhostname="$(get_main_cf 'myhostname')"

set_main_cf 'mydomain' "${domainname}"
new_mydomain="$(get_main_cf 'mydomain')"

set_main_cf 'myorigin' "${new_myhostname}"

set_main_cf 'inet_interfaces' 'all'

set_main_cf 'mydestination' "${new_myhostname}, localhost.${new_mydomain}, localhost, ${new_mydomain}"

set_main_cf 'home_mailbox' 'Maildir\/' #TODO: escape

set_main_cf 'smtpd_banner' "${new_myhostname} ESMTP unknown"

# SMTP-Auth
set_main_cf 'smtpd_sasl_auth_enable' 'yes'

set_main_cf 'smtpd_sasl_local_domain' "${new_myhostname}"

set_main_cf 'smtpd_repicipent_restrictions' 'permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination'

set_smtpd_conf 'pwcheck_method' 'saslauthd'

# 受信メールサイズ制限
set_main_cf 'message_size_limit' '10485760'

# dovecot基本設定
set_dovecot_conf 'protocols' 'imap imaps pop3 pop3s'

set_dovecot_conf 'mail_location' 'maildir\:\~\/Maildir' #TODO: escape

#set_dovecot 'default_mail_env' 'maildir:~/Maildir'

#set_dovecot 'valid_chroot_dirs' '/home'

if [ ${ret} -eq 0 ]; then
    remove_backup ${backup_files} 
    set_auto_start 'sendmail' 'off'
    stop_daemon 'sendmail'

    set_auto_start 'saslauthd' 'on'
    stop_daemon 'saslauthd'
    start_daemon 'saslauthd'
    make_Maildir

    set_auto_start 'postfix' 'on'
    stop_daemon 'postfix'
    start_daemon 'postfix'
    set_mta_is_postfix

    set_auto_start 'dovecot' 'on'
    stop_daemon 'dovecot'
    start_daemon 'dovecot'
else
    restore ${backup_files}
fi

exit ${ret}
