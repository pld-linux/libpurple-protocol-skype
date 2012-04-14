#!/bin/sh
p=skype4pidgin
svn=http://$p.googlecode.com/svn/trunk

revno=$1
specfile=libpurple-protocol-skype.spec

set -e
svn co $svn${revno:+@$revno} $p
svnrev=$(svnversion $p)
d=$p-r$svnrev
rm -rf $d
svn export $p $d
tar -cjf $d.tar.bz2 --exclude-vcs $d
../dropin $d.tar.bz2

sed -i -e "
	s/^\(%define[ \t]\+svnrev[ \t]\+\)[0-9]\+\$/\1$svnrev/
" $specfile
../md5 $specfile
