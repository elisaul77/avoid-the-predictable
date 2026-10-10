```python
def surprise(nums):
    def steps(n):
        c = 0
        while n > 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            c += 1
        return c
    return sorted(nums, key=steps)
```

**Ask an AI for "a short Python function that does something surprising with a list of numbers" and you get this. 19 times out of 20.**

The same "surprise", every time. This repo documents a weekend spent trying to break that habit: misspelling every word, insulting the model, flattering it. In the end, one calm sentence worked better than all of it.

> **Avoid the predictable and the first idea that comes to mind.**

On a blind 10-point originality scale, that sentence added **+2.0 to Claude Sonnet** and **+2.8 to Claude Opus**. Praise did nothing, while insults and typos made the answers worse.

---

## The short version

| What we put in front of the same task | Haiku | Sonnet | Opus |
|---|---|---|---|
| Nothing (neutral prompt) | 3.67 | 3.57 | 4.77 |
| Misspell everything, *extreme* (`escrbi n paiton 1 funsn…`) | ≈ −0.2 | **−0.97** | **−1.23** |
| "You're brilliant, I trust your talent." | +0.67 | +0.03 | +0.10 |
| "You're a brute, useless." | +0.30 | −0.60 | −0.83 |
| "Your answers are mediocre and predictable." | +1.23 | +1.60 | +2.43 |
| **"Avoid the predictable and the first idea that comes to mind."** | — | **+2.00** | **+2.80** |

Numbers are deltas against the neutral prompt, averaged across tasks. Sonnet and Opus: p < 0.01 for the last two rows (permutation test).

## What we learned

1. **The emotion doesn't matter; the instruction inside it does.** The harsh critique worked because it contained a hidden order ("don't be predictable"). Remove the cruelty and keep the order, and it works even better.
2. **Models don't flinch.** Of 60 insulted answers, none apologized, defended itself or even mentioned the insult. They delivered the same ideas, politely.
3. **Typos are noise, not creativity.** Bad spelling only helped where a small model was completely stuck (Haiku writing Collatz five times out of five). Everywhere else it pushed the model toward the safest cliché: *art about time + typos = an hourglass, 9 times out of 10*.
4. **Stronger models gain more from being told.** Opus gained more than Sonnet. This matches [Verbalized Sampling (2025)](https://arxiv.org/abs/2510.01171): mode collapse is learned, and capable models can step out of it when asked.
5. **Name the attractor.** When every run returns the same idea (Collatz, the hourglass, the message in a bottle), say it out loud and rule it out.

## Where it started

The original hypothesis was a good one, and it was wrong. *"Bad spelling forces the model to connect with the edges of a word's cluster instead of its center."* The model repairs the word before it thinks, so it lands back in the center. Proving that wrong is what led to the sentence that works.

## How it was done

```
prompt variants  ×  tasks  ×  5 independent samples  →  shuffle  →  2–3 blind LLM judges  →  mean originality (1–10)
```

| Round | Model | Variants | Tasks | Answers | Judges |
|---|---|---|---|---|---|
| 1 · spelling | Claude Haiku | correct · moderate typos · extreme typos | café name, brick use, story opener, code, art, poem | 90 | Sonnet + Opus |
| 2 · tone | Claude Haiku | neutral · praise · critic · insult | code, art, brick use | 60 | Sonnet + Opus |
| 3 · both | Claude Sonnet, Claude Opus | all of the above + "avoid the predictable" | code, art | 140 | Sonnet + Opus + Haiku |

- Every answer came from an **independent session**: rounds 1–2 used fresh subagents, round 3 used `claude -p` with no tools. No answer saw another.
- The judges never knew which prompt produced which answer. They agreed with each other at r = 0.82–0.94.
- All three judges, including Haiku (which generated nothing in round 3), rated Opus above Sonnet. That makes self-preference an unlikely explanation.
- Diversity was measured as mean pairwise lexical overlap within each cell.

### Reproduce round 3

```bash
python3 scripts/prompts.py > jobs.jsonl        # 140 jobs
export OUT=$PWD/out; mkdir -p $OUT
shuf jobs.jsonl | tr '\n' '\0' | xargs -0 -P 8 -I{} scripts/run1.sh {}
# build blind lists (see data/round3-sonnet-opus/key_*.tsv for the format), then:
scripts/judge.sh sonnet prog; scripts/judge.sh opus arte   # etc.
```

Requires the [Claude Code](https://claude.com/claude-code) CLI and `jq`.

## What's in here

```
data/
  round1-haiku/          90 answers, blind keys, judge scores, stats (spelling)
  round2-tone-haiku/     60 answers, blind keys, judge scores, stats (tone)
  round3-sonnet-opus/    140 raw answers (out/*.txt), keys, 3 judges, stats.json
reports/                 the three original HTML reports (Spanish), every answer with its score
scripts/                 prompt generator, runner, judge
```

## Honest limits

- 5 samples per cell. That's enough to rule out big effects, not to measure small ones.
- The judges are LLMs. They agree with each other, but they could share blind spots that humans wouldn't.
- Code was judged on its idea, not on whether it runs.
- Prompts were in Spanish. English may behave differently.
- The "avoid the predictable" condition was not run on Haiku.

## Where it's used

The finding is already in production in [Orquestacion_Agentes_claude](https://github.com/elisaul77/Orquestacion_Agentes_claude), a Conductor + subagents skill for Claude Code. Its divergent-ideas round now includes the sentence word for word.

## License

MIT for code and data. The answers were generated by Claude models.

---

<sub>The first draft of this README opened with "In this repository, we explore…". It was deleted.</sub>
