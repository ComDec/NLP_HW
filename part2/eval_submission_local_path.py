import argparse
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import mean_absolute_error
from transformers import AutoModelForCausalLM, AutoTokenizer

from submission import (
    your_config,
    your_post_processing,
    your_pre_processing,
    your_prompt,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_path",
        default="./llamadownload",
        help="Path to the locally converted Llama-2 Hugging Face folder.",
    )
    parser.add_argument(
        "--num_cases",
        type=int,
        default=35,
        help="Number of random 7-digit addition cases to evaluate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=123,
        help="Random seed for reproducible evaluation pairs.",
    )
    parser.add_argument(
        "--output",
        default="local_path_eval.json",
        help="Path to write evaluation results.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )

    config = your_config().copy()
    config["max_new_tokens"] = config.pop("max_tokens")
    config.pop("stop", None)

    prefix, suffix = your_prompt()
    rng = np.random.default_rng(args.seed)
    pairs = [
        (
            int(np.ceil(rng.uniform(1000000, 9999999))),
            int(np.ceil(rng.uniform(1000000, 9999999))),
        )
        for _ in range(args.num_cases)
    ]

    rows = []
    for int_a, int_b in pairs:
        prompt = prefix + your_pre_processing(f"{int_a}+{int_b}") + suffix
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                pad_token_id=tokenizer.eos_token_id,
                **config,
            )
        raw = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1] :],
            skip_special_tokens=True,
        )
        pred = your_post_processing(raw)
        rows.append(
            {
                "a": int_a,
                "b": int_b,
                "answer": int_a + int_b,
                "raw": raw,
                "pred": pred,
                "correct": pred == int_a + int_b,
            }
        )

    acc = sum(row["correct"] for row in rows) / len(rows)
    mae = mean_absolute_error(
        [row["answer"] for row in rows],
        [row["pred"] for row in rows],
    )

    result = {
        "model_id": args.model_path,
        "num_cases": len(rows),
        "metrics": {"acc": acc, "mae": mae},
        "rows": rows,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(result, indent=2))
    print(json.dumps(result["metrics"], indent=2))
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
