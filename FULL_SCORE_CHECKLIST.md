# HW3 Full-Score Checklist

## Rubric Summary

- Part 1 (`35 pts`)
  - `23 pts`: `part1/src/bpe.py` correctly implements `merge()`, `encode()`, and `decode()`.
  - `12 pts`: `part1/tests/test_tokenizer.py` contains valid tokenizer-property counterexamples, and the written answers explain the failures plus why non-trivial tokenizers generally cannot preserve concatenation.
- Part 2 (`65 pts`)
  - Notebook answers for Q3/Q4 are complete and the requested metrics are reported.
  - `part2/submission.py` keeps exactly the required config keys, uses `max_tokens >= 50`, avoids arithmetic hacks in pre/post-processing, and returns the student's netid/HF token.
  - Prompt-a-thon full credit requires either average accuracy `> 0.2` or average MAE `< 1e5` on 30 hidden 7-digit addition cases.

## Submit-Ready Checklist

- `part1/src/bpe.py`
  - Most-frequent bigram merge is correct.
  - Ties are broken by lexicographically smaller bigram.
  - Replacement is left-to-right and non-overlapping.
  - `encode()` applies learned merge rules in training order.
  - `decode()` reconstructs text by concatenating vocab entries.
- `part1/tests/test_tokenizer.py`
  - `test_not_injective()` passes.
  - `test_not_invertible()` passes.
  - `test_not_preserving_concat()` passes.
- Part 1 written answers
  - Explain the tokenizer chosen for each counterexample.
  - Explain the failure mode in at most two sentences each.
  - Explain why non-trivial tokenizers usually cannot preserve concatenation.
  - Disclose AI assistance usage.
- `part2/prompting_exercises.ipynb`
  - Q3/Q4 written cells are filled.
  - Q4b contains an updated post-processing function.
  - Reported Q4c metrics match the experiment outputs.
- `part2/submission.py`
  - `your_netid()` is filled.
  - `your_hf_token()` resolves to a usable Hugging Face token.
  - Prompt uses the final optimized few-shot format.
  - Pre-processing only reformats the input and does not compute the sum.
  - Post-processing only extracts the first plausible answer and does not compute the sum.
  - Config contains exactly `max_tokens`, `temperature`, `top_k`, `top_p`, `repetition_penalty`, and `stop`.
  - `max_tokens` is at least `50`.
- Local verification
  - Part 1 visible tests pass.
  - AST check confirms pre/post-processing contain no `+` operator hacks.
  - Proxy-Llama evaluation for the final prompt comfortably exceeds the full-credit threshold.

## Current Status

- Part 1 visible tests: passed.
- Part 2 syntax and anti-hack AST check: passed.
- Final prompt on public Llama-2 chat mirror (`NousResearch/Llama-2-7b-chat-hf`): `acc = 0.8`, `mae = 4055.17` on a 35-case local stress test (`part2/final_submission_eval.json`).
- Remaining external dependency: the class autograder still needs a Hugging Face token that has access to `meta-llama/Llama-2-7b-chat-hf`.
