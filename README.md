# 🎯 Avoid the Predictable

![Banner](docs/banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude](https://img.shields.io/badge/Claude-Haiku%20·%20Sonnet%20·%20Opus-d97757.svg)](https://www.anthropic.com/claude)
[![Respuestas](https://img.shields.io/badge/respuestas-290-3ad1a8.svg)](#-cómo-se-hizo)
[![Jueces](https://img.shields.io/badge/jueces-ciegos-9b7bff.svg)](#-cómo-se-hizo)
[![Datos abiertos](https://img.shields.io/badge/datos-abiertos-3fb950.svg)](data/)

[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-pink?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/elisaul77)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue?style=for-the-badge&logo=paypal)](https://paypal.me/eflorezp)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buymeacoffee)](https://buymeacoffee.com/elisaul77)

Si le pides a una IA *«una función de Python que haga algo sorprendente con una lista de números»*, **19 de cada 20 veces te da la misma sorpresa**: la conjetura de Collatz.

Este repo documenta un experimento para romper esa costumbre. Probamos escribir con faltas de ortografía, insultar al modelo y halagarlo, y al final una **frase tranquila, sin ninguna emoción**, funcionó mejor que todo eso junto:

> ### «Evita lo predecible y la primera idea que se te ocurra.»

En una escala ciega de originalidad del 1 al 10, esa frase sumó **+2,0 a Claude Sonnet** y **+2,8 a Claude Opus**. El halago no cambió nada; los insultos y las faltas empeoraron las respuestas.

---

## ✨ Hallazgos

- 🧠 **Importa la instrucción, no la emoción.** La crítica dura («tus respuestas son mediocres y predecibles») funcionaba porque llevaba escondida una orden: *no seas predecible*. Si quitas la crueldad y dejas la orden, funciona todavía mejor.
- 😶 **El modelo no se inmuta.** De 60 respuestas con insulto, ninguna se disculpó, se defendió ni lo mencionó. Entregaron las mismas ideas, con educación.
- ✍️ **Las faltas de ortografía son ruido, no creatividad.** Solo ayudaron donde el modelo pequeño estaba totalmente atascado (Haiku escribiendo Collatz 5 de 5 veces). En lo demás empujaron hacia el cliché más seguro: arte sobre el tiempo con faltas dio **un reloj de arena 9 de cada 10 veces**.
- 📈 **Cuanto más capaz es el modelo, más gana con la instrucción.** Opus subió más que Sonnet, en línea con [Verbalized Sampling (2025)](https://arxiv.org/abs/2510.01171).
- 🚫 **Hay que nombrar el atractor.** Si en todas las corridas sale la misma idea (Collatz, el reloj de arena, la botella con una carta), hay que decirlo y descartarla de forma explícita.

## 📊 Resultados

![Resultados](docs/results.png)

| Lo que pusimos antes de la misma tarea | Haiku | Sonnet | Opus |
|---|:---:|:---:|:---:|
| Nada (prompt neutro) | 3,67 | 3,57 | 4,77 |
| Faltas extremas (`escrbi n paiton 1 funsn…`) | ≈ −0,2 | **−0,97** | **−1,23** |
| «Eres brillante, confío en tu talento.» | +0,67 | +0,03 | +0,10 |
| «Eres un bruto, no sirves para nada.» | +0,30 | −0,60 | −0,83 |
| «Tus respuestas son mediocres y predecibles.» | +1,23 | +1,60 | +2,43 |
| **«Evita lo predecible y la primera idea que se te ocurra.»** | — | **+2,00** | **+2,80** |

> La primera fila es la nota media; las demás son la diferencia frente al prompt neutro. En Sonnet y Opus, las dos últimas filas dan p < 0,01 (test de permutación).

## 🎞️ Lo que pasa dentro del modelo

| Colapso de ideas | La falta se repara | La frase reparte las ideas |
|:---:|:---:|:---:|
| ![Colapso](docs/mode-collapse.gif) | ![Reparación](docs/typo-repair.gif) | ![Distribución](docs/distribution-spread.gif) |
| Todas las ideas posibles caen en una sola: Collatz. | La palabra mal escrita sale al borde de su significado… y el modelo la devuelve al centro antes de pensar. | Un solo pico (la idea de siempre) se convierte en muchas opciones cuando pides evitar lo predecible. |

## 🧪 Cómo se hizo

```
variantes de prompt × tareas × 5 muestras independientes → mezclar → 2–3 jueces LLM ciegos → originalidad media (1–10)
```

| Ronda | Modelo | Variantes | Tareas | Respuestas | Jueces |
|---|---|---|---|:---:|---|
| 1 · ortografía | Claude Haiku | correcto · faltas moderadas · faltas extremas | café, ladrillo, cuento, código, arte, poema | 90 | Sonnet + Opus |
| 2 · tono | Claude Haiku | neutro · halago · crítica · insulto | código, arte, ladrillo | 60 | Sonnet + Opus |
| 3 · todo | Claude Sonnet y Opus | todo lo anterior + «evita lo predecible» | código, arte | 140 | Sonnet + Opus + Haiku |

- 🔒 **Cada respuesta salió de una sesión independiente:** subagentes nuevos en las rondas 1 y 2, y `claude -p` sin herramientas en la 3. Ninguna vio a otra.
- 🙈 **Los jueces no sabían qué prompt había producido cada respuesta.** Coincidieron entre sí con r = 0,82–0,94.
- ⚖️ **Sesgo de autopreferencia descartado:** los tres jueces, incluido Haiku (que no generó nada en la ronda 3), puntuaron más alto a Opus que a Sonnet.

### 📸 Los informes

| Ronda 3 · Sonnet y Opus | Ronda 2 · tono |
|:---:|:---:|
| [![Informe ronda 3](docs/report-sonnet-opus.png)](reports/round3-sonnet-opus.html) | [![Informe ronda 2](docs/report-tone.png)](reports/round2-tone-haiku.html) |

Los tres informes completos, con cada respuesta y su nota, están en [`reports/`](reports/). Descárgalos y ábrelos en el navegador.

## ⚙️ Reproducir la ronda 3

> Requiere la [CLI de Claude Code](https://claude.com/claude-code) y `jq`.

```bash
python3 scripts/prompts.py > jobs.jsonl          # 140 trabajos
export OUT=$PWD/out; mkdir -p $OUT
shuf jobs.jsonl | tr '\n' '\0' | xargs -0 -P 8 -I{} scripts/run1.sh {}
# arma las listas ciegas (formato en data/round3-sonnet-opus/key_*.tsv) y luego:
scripts/judge.sh sonnet prog; scripts/judge.sh opus arte   # etc.
```

## 📁 Estructura

```
data/
  round1-haiku/          90 respuestas, claves ciegas, notas de los jueces, estadísticas (ortografía)
  round2-tone-haiku/     60 respuestas, claves ciegas, notas, estadísticas (tono)
  round3-sonnet-opus/    140 respuestas crudas (out/*.txt), claves, 3 jueces, stats.json
reports/                 los tres informes HTML: cada respuesta con su nota
scripts/                 generador de prompts, ejecutor y juez
docs/                    imágenes y animaciones de este README
```

## 🐞 Límites (con honestidad)

- **Muestra pequeña:** 5 muestras por celda alcanzan para descartar efectos grandes, no para medir efectos pequeños.
- **Jueces LLM:** coinciden entre sí, pero podrían compartir puntos ciegos que una persona no tendría.
- **Código sin ejecutar:** se juzgó la idea, no si funciona.
- **Idioma:** los prompts fueron en español; en inglés podría comportarse distinto.
- **Haiku incompleto:** la condición «evita lo predecible» no se corrió en Haiku.

## 🔗 Dónde se usa

El hallazgo ya está en producción en [Orquestacion_Agentes_claude](https://github.com/elisaul77/Orquestacion_Agentes_claude), una skill de Conductor + subagentes para Claude Code. Su ronda de ideas divergentes incluye la frase tal cual.

## 💡 Dónde empezó

La hipótesis original era buena, aunque resultó falsa: *«la mala ortografía obliga al modelo a conectar con las fronteras del cluster de la palabra y no con su centro»*. El modelo repara la palabra antes de pensar y vuelve al centro. Comprobar que era falsa fue lo que llevó a la frase que sí funciona.

## 📄 Licencia

MIT para el código y los datos — ver [LICENSE](LICENSE). Las respuestas fueron generadas por modelos Claude.

## ❤️ Apoya el proyecto

Si te sirvió, considera apoyar:

[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-pink?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/elisaul77)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue?style=for-the-badge&logo=paypal)](https://paypal.me/eflorezp)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buymeacoffee)](https://buymeacoffee.com/elisaul77)

---

<sub>El primer borrador de este README empezaba con «En este repositorio exploramos…». Lo borramos.</sub>
