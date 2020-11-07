#!/bin/bash


sTimestamp=$(date "+%Y/%m/%d %H:%M:%S")
nProcessLaunched=$(ps -aef | grep -i "check_presence\.py" | grep -v grep | wc -l)
if [ "${nProcessLaunched}" -gt 0 ]; then
        echo "${sTimestamp} check_presence already launched, skipping..." >&2
        exit 1
fi

echo "${sTimestamp} INFO launching check_presence script monitoring..."

cd /usr/local/scripts/jeedom-scripts
. venv/bin/activate > /dev/null 2>&1
python ./bin/check_presence.py 2>&1
nExitCode=$?
deactivate > /dev/null 2>&1

exit ${nExitCode}

