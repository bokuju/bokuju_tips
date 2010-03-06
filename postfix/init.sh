#!/bin/bash

###
# Including
#
if [ -f $(pwd $0)/.postfix.sh ]; then
    source $(pwd $0)/.postfix.sh
fi

###
# Settings
#
ret=0
domainname="$(get_domainname $(hostname))"

###
# Main
#
backup ${backup_files}

# 基本設定
set_main_cf 'myhostname' "mail.${domainname}"
new_myhostname="$(get_main_cf 'myhostname')"

set_main_cf 'mydomain' "${domainname}"
new_mydomain="$(get_main_cf 'mydomain')"

set_main_cf 'myorigin' "${new_myhostname}"

set_main_cf 'inet_interfaces' 'all'

set_main_cf 'mydestination' "${new_myhostname}, localhost.${new_mydomain}, localhost, ${new_mydomain}"

set_main_cf 'home_mailbox' 'Maildir\/'

set_main_cf 'smtpd_banner' "${new_myhostname} ESMTP unknown"

# SMTP-Auth

# 受信メールサイズ制限

if [ ${ret} -eq 0 ]; then
    remove_backup ${backup_files} 
else
    restore ${backup_files}
fi

exit ${ret}
