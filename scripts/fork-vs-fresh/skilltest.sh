#!/bin/bash
# skilltest.sh <sessfile> <id>
X=$(cd "$(dirname "$0")" && pwd); S=$(cat $X/$1); id=K$2; W=$X/runs/$id
rm -rf $W; cp -r $X/fixture $W
enc(){ echo "$1" | sed 's/[^a-zA-Z0-9]/-/g'; }
mkdir -p ~/.claude/projects/$(enc $W); cp ~/.claude/projects/$(enc $X/runs/base)/$S.jsonl ~/.claude/projects/$(enc $W)/
P='/subagent-pool Necesito total_factura(items, cupon=None) en tienda/factura.py que devuelva el total a cobrar. items es una lista de (codigo, cantidad). Cupones: BIENVENIDA10 = 10 % de descuento; FIJO5000 = resta 5000 pesos sin dejar el gravado en negativo; cualquier otro cupón es error. Un producto desconocido también es error. Delega la implementación (proceed without context, no hay project-context). Plan aprobado de antemano: no me pidas confirmación, hazlo y repórtame.'
cd $W && CLAUDE_CODE_FORK_SUBAGENT=1 timeout 1500 claude -p --model sonnet --resume $S --fork-session --permission-mode bypassPermissions --output-format json "$P" > $X/res3_$id.json 2>&1
s=$(jq -r .session_id $X/res3_$id.json)
echo "$id cost=$(jq .total_cost_usd $X/res3_$id.json) agents=$(cat ~/.claude/projects/$(enc $W)/$s/subagents/*.meta.json 2>/dev/null | jq -r .agentType | tr '\n' ,) score=$(python3 $X/hidden/check.py $W A | jq -c '[.[]]|add')/13"
