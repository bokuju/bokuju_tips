#!/bin/sh

if [ -f $(dirname $0)/.mail_conf.sh ]; then
    source $(dirname $0)/.mail_conf.sh
fi

SUBJECT="Today Weather News"

BODY=`cat<<_EOT_
$($(dirname $0)/get_otenki.py)
_EOT_`

echo -e "${BODY}" | env from=${FROM} smtp=${SERVER} \
   smtp-auth-user=${AUTH_USER} smtp-auth-password=${AUTH_PASSWD} \
   smtp-auth=login mailx -n -s "${SUBJECT}" ${TO}
