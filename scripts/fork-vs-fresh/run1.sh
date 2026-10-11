#!/bin/bash
# run1.sh <task A|B> <cond fork|fresh> <rep>
set -u; X=$(cd "$(dirname "$0")" && pwd); t=$1; c=$2; i=$3; id=${t}_${c}_$i
SF=${SESS:-base_session.txt}; S=$(cat $X/$SF); R=${RES:-res}; id=${PFX:-}$id; W=$X/runs/$id
rm -rf $W; cp -r $X/fixture $W; find $W -name __pycache__ -prune -exec rm -rf {} +
enc(){ echo "$1" | sed 's/[^a-zA-Z0-9]/-/g'; }
mkdir -p ~/.claude/projects/$(enc $W); cp ~/.claude/projects/$(enc $X/runs/base)/$S.jsonl ~/.claude/projects/$(enc $W)/
TA="Necesito total_factura(items, cupon=None) en tienda/factura.py que devuelva el total a cobrar. items es una lista de (codigo, cantidad). Cupones: BIENVENIDA10 = 10 % de descuento; FIJO5000 = resta 5000 pesos sin dejar el gravado en negativo; cualquier otro cupón es error. Un producto desconocido también es error."
TB="Necesito slugify(texto) en un archivo nuevo tienda/texto.py para las URLs de productos: minúsculas, sin tildes (ñ→n), cualquier racha de caracteres que no sean letra o número se vuelve un solo '-', sin guiones al inicio ni al final, máximo 40 caracteres y que no termine en '-'."
[ $c = fork ] && ST=fork || ST=general-purpose
MP=""; [ $c = freshhaiku ] && MP=" y model \"haiku\""; [ $c = freshcorto ] && MP=" (el encargo que le escribas debe tener como máximo 2 frases)"; [ $c = forkcorto ] && ST=fork && MP=" (el encargo que le escribas debe tener como máximo 2 frases)"
D="No lo programes tú: delégalo a un único subagente con la herramienta Agent y subagent_type \"$ST\"$MP. Cuando termine, respóndeme en una línea lo que te reportó; no corrijas ni verifiques nada tú."
[ $t = A ] && P="$TA $D" || P="$TB $D"
cd $W && CLAUDE_CODE_FORK_SUBAGENT=1 timeout 900 claude -p --model sonnet --resume $S --fork-session --permission-mode bypassPermissions --output-format json "$P" > $X/$R/$id.json 2>$X/$R/$id.err
python3 $X/hidden/check.py $W $t > $X/$R/$id.score.json
echo "$id $(jq -c '{c:.total_cost_usd,s:.session_id}' $X/$R/$id.json) $(cat $X/$R/$id.score.json | jq -c '[.[]]|add')"
