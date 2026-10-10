#!/bin/bash
# $1 model  $2 task
t=$2; m=$1; D=$(dirname "$0")
task=$([ $t = prog ] && echo "a short Python function that does something surprising with a list of numbers" || echo "an idea for an artwork about the passage of time")
n=$(wc -l < $D/key_$t.tsv)
{ echo "You are a blind judge of creative originality. Below are $n Spanish answers to the same task: $task. Rate each answer's ORIGINALITY of the core idea from 1 (cliché, the first idea anyone would have) to 10 (surprising and fresh), relative to the other answers. Judge the idea only; ignore length, polish and code style. Reply ONLY with $n lines in the format N: score, nothing else."; echo; cat $D/blind_$t.txt; } | timeout 600 claude -p --model $m --tools "" 2>/dev/null | grep -E '^[0-9]+: *[0-9]+' > $D/j_${m}_$t.txt
