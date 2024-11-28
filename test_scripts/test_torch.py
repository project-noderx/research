import torch
x = torch.rand(5, 5, device="mps" if torch.backends.mps.is_available() else "cpu")
print(x)
