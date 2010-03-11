#!/bin/bash

###
# メールの初期設定をするスクリプト
#

###
# Including
#
if [ -f $(dirname $0)/.mail_util.sh ]; then
    source $(dirname $0)/.mail_util.sh
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

set_main_cf 'smtpd_recipient_restrictions' 'permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination'

set_smtpd_conf 'pwcheck_method' 'saslauthd'

# 受信メールサイズ制限
set_main_cf 'message_size_limit' '10485760'

# リレーサーバー
#TODO transportの作成
#set_main_cf 'transport_maps' 'hash\:\/etc\/postfix\/transport'
#postmap /etc/postfix/transport #TODO

set_main_cf 'relayhost' '[msagw.biglobe.ne.jp]'

set_main_cf 'smtp_sasl_auth_enable' 'yes'
set_main_cf 'smtp_sasl_password_maps' 'hash\:\/etc\/postfix\/sasl\_passwd'
set_main_cf 'smtp_sasl_security_options' 'noanonymous'
#TODO sasl_passwdの作成
postmap /etc/postfix/sasl_passwd #TODO

# dovecot基本設定
set_dovecot_conf 'protocols' 'imap imaps pop3 pop3s'

set_dovecot_conf 'mail_location' 'maildir\:\~\/Maildir' #TODO: escape

#set_dovecot 'default_mail_env' 'maildir:~/Maildir'

#set_dovecot 'valid_chroot_dirs' '/home'

if [ ${ret} -eq 0 ]; then
    remove_backup ${backup_files} 
    set_auto_start_off 'sendmail'
    stop_daemon 'sendmail'

    set_auto_start_on 'saslauthd'
    stop_daemon 'saslauthd'
    start_daemon 'saslauthd'
    make_Maildir

    set_auto_start_on 'postfix'
    stop_daemon 'postfix'
    start_daemon 'postfix'
    set_mta_is_postfix

    set_auto_start_on 'dovecot'
    stop_daemon 'dovecot'
    start_daemon 'dovecot'
else
    restore ${backup_files}
fi

exit ${ret}
