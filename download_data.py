from datasets import load_dataset


ds = load_dataset("amitayusht/PutnamBench")

print(ds["train"][0])

print(ds["train"][0].keys())