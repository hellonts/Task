#!/bin/bash
a="`find ./   -name .svn`"
for b in $a
do
	rm -rf $b
	echo $b
done
