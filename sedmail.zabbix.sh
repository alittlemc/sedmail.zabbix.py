#!/bin/bash
cd `dirname $0`
echo "{ALERT.SENDTO} = $1" > debug.txt
echo "{ALERT.SUBJECT} = $2" >> debug.txt
echo "{ALERT.MESSAGE} = $3" >> debug.txt
if [[ $4 -gt 10 ]]
then
  python3 sedmail.zabbix.py "$1" "$2" "$3" >> debug.txt
else
  python3 sedmail.zabbix-qq.py "$1" "$2" "$3" >> debug.txt
fi

echo "shell success" >> debug.txt
find graph -type f -name "*.png" | xargs rm
#删除所有的图片
