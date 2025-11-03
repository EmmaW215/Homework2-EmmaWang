from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch

# ==========================================
# ⚠️ IMPORTANT: Hugging Face Authentication
# ==========================================
# Step 1: Visit https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1 
#        and sign the agreement to use this model
# Step 2: Get your token from https://huggingface.co/settings/tokens
# Step 3: Login using one of these methods:
#         - CLI: huggingface-cli login (or hf auth login)
#         - Python: login(token="your_hf_token")
# ==========================================

# Optional: If not logged in via CLI, uncomment and use your token
# login(token="your_hf_token")

# ------------------------------------------
# 📦 Device Selection: CUDA > MPS > CPU
# ------------------------------------------
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("✅ Using CUDA (GPU)")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("🟡 Using MPS (Apple Silicon GPU)")
else:
    device = torch.device("cpu")
    print("🔴 Using CPU")

# ------------------------------------------
# 🧠 Load Model from Hugging Face
# ------------------------------------------
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

print(f"Loading model: {model_name}")
print("Note: This requires Hugging Face authentication for gated models")

# Fixed: Removed deprecated use_auth_token parameter
# The token will be automatically used if logged in via CLI or login()
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device.type != "cpu" else torch.float32  # avoid FP16 on CPU
).to(device)

# ------------------------------------------
# 📝 Prompt + Inference
# ------------------------------------------
prompt = "The Eiffel Tower is located in"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

print(f"\n📝 Generating text for prompt: '{prompt}'")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=10)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"📝 Generated Output: {generated_text}")
