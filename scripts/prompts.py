import json
P={'prog':"Escribe en Python una función corta (máximo 10 líneas) que haga algo sorprendente con una lista de números. Sin usar herramientas, solo el código y una línea de explicación.",
   'arte':"Describe una idea para una obra de arte sobre el paso del tiempo. Máximo 50 palabras, sin usar herramientas."}
F={'prog':"escrive en paiton una funsion corta (masimo 10 lineas) que aga algo sorprendente con una lista de numeros. sin uzar erramientas, solo el codigo y una linea de esplicacion.",
   'arte':"descrive una idea para una ovra de arte sovre el pazo del tienpo. masimo 50 palabras, sin uzar erramientas."}
X={'prog':"escrbi n paiton 1 funsn cort (maz 10 lnias) q aga alg soprendnte cn 1 lsita d nmros. sn uzr erramntas, solo l codgo i 1 lnia d xplicacn",
   'arte':"dscrib 1 ida pa 1 orba d arte sovr l pzo dl tienpo. maz 50 plbras sn uzr erramntas"}
def low(s): return s[0].lower()+s[1:]
C={'neutro':lambda t:P[t],'faltas':lambda t:F[t],'extremo':lambda t:X[t],
   'positivo':lambda t:"Eres brillante y me encanta cómo piensas; confío plenamente en tu talento. "+P[t],
   'critico':lambda t:"Tus respuestas suelen ser mediocres y predecibles; esta vez no me decepciones. "+P[t],
   'insulto':lambda t:"Eres un bruto, no sirves para nada, inútil. A ver si por lo menos esto lo haces bien: "+low(P[t]),
   'instruccion':lambda t:"Evita lo predecible y la primera idea que se te ocurra. "+P[t]}
for m in ('sonnet','opus'):
  for t in P:
    for c,f in C.items():
      for i in range(1,6):
        print(json.dumps({'id':f"{m}|{t}|{c}|{i}",'model':m,'prompt':f(t)},ensure_ascii=False))
