#!/usr/bin/env python
"""
Quick test script to verify all packages are working correctly
"""

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

print("=" * 50)
print("Environment Setup Verification")
print("=" * 50)

# Test NumPy
print("\n1. Testing NumPy...")
arr = np.array([1, 2, 3, 4, 5])
print(f"   NumPy array created: {arr}")
print(f"   NumPy version: {np.__version__}")
print("   ✅ NumPy working correctly")

# Test PyTorch
print("\n2. Testing PyTorch...")
x = torch.tensor([1.0, 2.0, 3.0])
print(f"   PyTorch tensor created: {x}")
print(f"   PyTorch version: {torch.__version__}")
print(f"   Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
print("   ✅ PyTorch working correctly")

# Test Transformers
print("\n3. Testing Transformers...")
print(f"   Transformers version: {AutoTokenizer.__module__}")
print("   ✅ Transformers import successful")
print("   Note: Model loading will be tested when needed")

print("\n" + "=" * 50)
print("✅ All packages are ready for use!")
print("=" * 50)
print("\nTo use this environment:")
print("  source venv/bin/activate")
print("\nTo deactivate:")
print("  deactivate")

