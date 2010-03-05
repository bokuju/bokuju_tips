#!/bin/bash

if [ -f $(pwd $0)/common.sh ]; then
    source $(pwd init.sh)/common.sh
fi

ret=0

backup ${backup_files}

set_key_eq_value "${main_cf}" 'myhostname' "mail.$(get_domainname $(hostname))"
set_key_eq_value "${main_cf}" 'mydomain' "$(get_domainname $(hostname))"
set_key_eq_value "${main_cf}" 'myorigin' "$(get_key_eq_value "${main_cf}" 'myhostname')"

if [ ${ret} -eq 0 ]; then
    remove_backup ${backup_files} 
else
    restore ${backup_files}
fi

exit ${ret}
