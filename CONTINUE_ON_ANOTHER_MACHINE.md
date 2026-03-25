# Continue On Another Machine

## Files that matter

Keep these submission files:

- `part1_written_answers.pdf`
- `part1/src/bpe.py`
- `part1/tests/test_tokenizer.py`
- `part2/submission.py`
- `part2/prompting_exercises.ipynb`

Helpful local-only files:

- `FULL_SCORE_CHECKLIST.md`
- `part2/LOCAL_LLAMA2_SETUP.md`
- `part2/eval_submission_local_path.py`
- `part2/final_submission_eval.json`

## On the next machine

1. Copy the whole `hw3/` folder.
2. Follow `part2/LOCAL_LLAMA2_SETUP.md` to download and convert the official Llama-2 7B-chat weights from Meta.
3. Temporarily set `model_id_1` in `part2/prompting_exercises.ipynb` to the local converted folder path.
4. Run notebook experiments if needed.
5. Run local prompt validation:

```bash
cd part2
python eval_submission_local_path.py --model_path /absolute/path/to/llamadownload
```

6. Before upload, restore the notebook text to:

```python
model_id_1 = "meta-llama/Llama-2-7b-chat-hf"
```

## What not to upload

- Downloaded Meta weight folders
- Converted local `llamadownload/` folder
- Local-only eval outputs such as `local_path_eval.json`
- Any modified grader/helper files used only for local testing
