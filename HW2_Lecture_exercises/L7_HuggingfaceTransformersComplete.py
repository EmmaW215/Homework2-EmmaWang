from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"MPS available: {torch.backends.mps.is_available()}")


model_name = "openchat/openchat-3.5-1210"

# Step 1: Load tokenizer (lightweight, always works)
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Step 2: Detect best available device
if torch.cuda.is_available():
    device = "cuda"
    dtype = torch.float16
    print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    device = "mps"  # Apple Silicon
    dtype = torch.float16
    print("Using Apple MPS (Metal Performance Shaders)")
else:
    device = "cpu"
    dtype = torch.float32  # CPU doesn't support FP16 well
    print("⚠️ Using CPU - this will be SLOW!")

# Step 3: Load model with appropriate settings
print(f"Loading model in {dtype}...")
try:
    # Try with device_map first (requires accelerate)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=dtype,
        device_map="auto",
        low_cpu_mem_usage=True  # Reduces RAM usage during loading
    )
    print("✅ Model loaded with device_map")
except Exception as e:
    print(f"⚠️ device_map failed: {e}")
    print("Falling back to manual device placement...")
    
    # Fallback: load without device_map
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=dtype
    ).to(device)
    print(f"✅ Model loaded to {device}")

# Step 4: Test the model
print("\nTesting model...")
prompt = "What is machine learning?"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        temperature=0.7
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"\nPrompt: {prompt}")
print(f"Response: {response}")