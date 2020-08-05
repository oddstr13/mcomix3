#!/bin/sh
ROOTDIR="mcomix"
VERSION=$(grep __version__ $ROOTDIR/__init__.py | sed -e "s/__version__\s*=\s*//" -e "s/['\"\s]//g")
MAINTAINER="NAME@HO.ST"

xgettext -LPython -omcomix.pot -p$ROOTDIR/messages/ -cTRANSLATORS \
    --from-code=utf-8 --package-name=MComix --package-version=${VERSION} \
    --msgid-bugs-address=${MAINTAINER} \
    $ROOTDIR/**.py

for pofile in $ROOTDIR/messages/*/LC_MESSAGES/*.po
do
    echo -n "$pofile "
    # Merge message files with master template, no fuzzy matching (-N)
    msgmerge -U --backup=none ${pofile} $ROOTDIR/messages/mcomix.pot
    # Compile translation, add "-f" to include fuzzy strings
    #msgfmt ${pofile} -o ${pofile%.*}.mo
done
