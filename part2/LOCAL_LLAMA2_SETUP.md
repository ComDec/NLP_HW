# Local Llama-2 Setup

Use this only for local experimentation when your Meta approval email has arrived but Hugging Face gated access is still pending.

## 1. Download official Llama-2 weights from Meta

```bash
git clone https://github.com/meta-llama/llama.git
cd llama

# Paste the download link from the approval email: "Get started with Llama 2"
# Select 7B-chat
bash download.sh

mv tokenizer.model llama-2-7b-chat/tokenizer.model
mv tokenizer_checklist.chk llama-2-7b-chat/tokenizer_checklist.chk

wget https://raw.githubusercontent.com/huggingface/transformers/refs/heads/main/src/transformers/models/llama/convert_llama_weights_to_hf.py
python convert_llama_weights_to_hf.py --input_dir ./llama-2-7b-chat --model_size 7B --output_dir ./llamadownload --llama_version 2
```

The converted Hugging Face-style model folder will be `./llamadownload`.

## 2. Point the notebook to the local folder

In `part2/prompting_exercises.ipynb`, replace `model_id_1` with the absolute path to the converted folder, for example:

```python
model_id_1 = "/absolute/path/to/llamadownload"
```

If you only want a clean upload version, you can keep the uploaded notebook text as `meta-llama/Llama-2-7b-chat-hf` and use the local path only while running experiments.

## 3. Run local validation without Hugging Face access

From `part2/`, run:

```bash
python eval_submission_local_path.py --model_path /absolute/path/to/llamadownload
```

This writes `local_path_eval.json` with accuracy and MAE for 35 random 7-digit addition cases.

## 4. Optional warning cleanup

If generation prints:

```text
Setting pad_token_id to eos_token_id:2 for open-end generation.
```

you can silence it by passing:

```python
pad_token_id=tokenizer.eos_token_id
```

inside the `model.generate(...)` call used in the notebook or local test harness.

## 5. Important submission note

- This workaround is for local experimentation.
- Do not submit a modified grader file.
- The required submission files remain:
  - `part1_written_answers.pdf`
  - `part1/src/bpe.py`
  - `part1/tests/test_tokenizer.py`
  - `part2/submission.py`
  - `part2/prompting_exercises.ipynb`
