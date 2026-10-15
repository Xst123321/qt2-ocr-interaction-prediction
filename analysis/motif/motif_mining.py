import torch
import numpy as np
import h5py
import pickle
from captum.attr import IntegratedGradients
from model import Net
import sys

sys.path.insert(0, '/mnt/e/work/QT2_analysis/06_model/code')

device = torch.device("cuda:0")
net = Net().to(device)
net.load_state_dict(torch.load('/mnt/e/work/QT2_analysis/06_model/code/model_weights.pth'))
net.eval()

# 加载正样本（前 150115 个）
data_dir = '/mnt/e/work/QT2_analysis/06_model/data'
anchor1 = np.load(f'{data_dir}/anchor1.npy', mmap_mode='r')
anchor2 = np.load(f'{data_dir}/anchor2.npy', mmap_mode='r')

# 用测试集的正样本（前 150115 个里的最后 20%）
n_pos = 150115
test_start = int(n_pos * 0.8)
test_end = n_pos

# 取 500 个高置信度正样本做 IG 分析（太多会很慢）
np.random.seed(42)
sample_idx = np.random.choice(range(test_start, test_end), size=500, replace=False)

# Integrated Gradients
ig = IntegratedGradients(net)

def predict_fn(x):
    """包装模型，用于 Captum"""
    return net(x)

all_attributions = []

for i, idx in enumerate(sample_idx):
    a1 = torch.tensor(anchor1[idx], dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
    a2 = torch.tensor(anchor2[idx], dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
    seq = torch.cat([a1, a2], dim=3)

    # 基线：全零
    baseline = torch.zeros_like(seq)

    try:
        attr = ig.attribute(seq, baselines=baseline, target=1, n_steps=50)
        # attr shape: (1, 1, 4, 6000)
        attr_np = attr.squeeze().cpu().detach().numpy()  # (4, 6000)
        # 每个位置的贡献 = 4 个通道的绝对值之和
        per_pos = np.abs(attr_np).sum(axis=0)  # (6000,)
        all_attributions.append(per_pos)
    except Exception as e:
        print(f'Sample {i} failed: {e}')
        continue

    if (i + 1) % 50 == 0:
        print(f'Processed {i+1}/{len(sample_idx)}')

all_attributions = np.array(all_attributions)  # (500, 6000)
np.save('attributions.npy', all_attributions)
print(f'Done. Shape: {all_attributions.shape}')
