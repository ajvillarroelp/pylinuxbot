#!/bin/bash
#$1 pptx files
#$2 line
unzip $1 -d /tmp/pp.$$ > /dev/null
SLIDES_LIST=$(unzip -l $1 | grep slides/sli | tr -s " " | cut -d " " -f 5 | sort --version-sort | xargs)
cd /tmp/pp.$$
x=0
for i in $SLIDES_LIST; do
    x=$( echo "$x + 1" | bc )
    if [[ $x == $2 ]]; then
#cat $i | grep -oP '<a:t>(.*)</a:t>' | sed 's|<[^>]*>| |g' | sed 's|&.*;||g' | cut -d" " -f 1,2,3,4
cat $i | sed 's|&.*;||g' | awk 'BEGIN{IGNORECASE=1;FS="<a:t>|</a:t>";RS=EOF} { if ($2 != "" ) { print $2} else {print $4 }}'
#| awk -F"</a:t>" '{print $2;}'
    fi
done
rm -rf /tmp/pp.$$
#| sed 's/<\/a:t>//g'
