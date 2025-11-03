from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "openchat/openchat-3.5-1210"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16,  # 👈 Fixed: Changed from torch_dtype
    device_map="auto"     # 👈 This needs accelerate
)