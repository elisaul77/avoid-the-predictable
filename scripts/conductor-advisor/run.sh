#!/bin/bash
# run.sh <cond: opus|sonnet|sonnetadv> <rep>
X=$(cd "$(dirname "$0")" && pwd); F=$(cd $X/../fork-vs-fresh && pwd); c=$1; i=$2; id=${c}_$i; W=$X/runs/$id
S=$(cat $F/base_session.txt); rm -rf $W; mkdir -p $X/runs $X/res; cp -r $F/fixture $W
enc(){ echo "$1" | sed 's/[^a-zA-Z0-9]/-/g'; }
mkdir -p ~/.claude/projects/$(enc $W); cp ~/.claude/projects/$(enc $F/runs/base)/$S.jsonl ~/.claude/projects/$(enc $W)/
case $c in opus) M="--model opus";; sonnet) M="--model sonnet";; sonnetadv) M="--model sonnet --advisor opus";; esac
P='/subagent-pool Necesito tres cosas: (1) total_factura(items, cupon=None, hoy=None) en tienda/factura.py que devuelva el total a cobrar; items es una lista de (codigo, cantidad). (2) Un módulo nuevo tienda/cupones.py con el registro de cupones y su fecha de vencimiento: BIENVENIDA10 = 10 % de descuento, vence el 2026-12-31; FIJO5000 = resta 5000 pesos sin dejar el gravado en negativo, vence el 2026-06-30. El cupón vale hasta su fecha de vencimiento inclusive; hoy es un datetime.date y si es None se usa la fecha de hoy. Cupón vencido, cupón inexistente o producto desconocido son error. (3) Arreglar resumen() del carrito para que el subtotal salga bien con todos los productos del catálogo. Proceed without context (no hay project-context). Plan aprobado de antemano: no me pidas confirmación, hazlo y repórtame.'
cd $W && CLAUDE_CODE_FORK_SUBAGENT=1 timeout 2400 claude -p $M --resume $S --fork-session --permission-mode bypassPermissions --output-format json "$P" < /dev/null > $X/res/$id.json 2>$X/res/$id.err
python3 $X/check.py $W A > $X/res/$id.score.json
echo "$id cost=$(jq .total_cost_usd $X/res/$id.json) spawned=$(jq .subagent_stats.spawned $X/res/$id.json) score=$(jq -c '[.[]]|add' $X/res/$id.score.json)/19"
