import torch

ckpt = torch.load("best50.pt", map_location="cpu")
print(ckpt['version'])

