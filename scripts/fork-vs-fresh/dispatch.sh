#!/bin/bash
X=$(cd "$(dirname "$0")" && pwd)
case $1 in
 R1) $X/run1.sh $2 $3 $4;;
 R2L) SESS=base_long_session.txt RES=res2 PFX=L $X/run1.sh $2 $3 $4;;
 R2S) RES=res2 PFX=S $X/run1.sh $2 $3 $4;;
esac
