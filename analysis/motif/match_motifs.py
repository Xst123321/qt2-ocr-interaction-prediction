import numpy as np
import sys
sys.path.insert(0, '/mnt/e/work/qt2-ocr-interaction-prediction/analysis/motif')

from parse_jaspar import parse_jaspar
from pyfaidx import Fasta

# 加载参考基因组
genome = Fasta('/mnt/e/group_data/atac/whfs-xs-190174_ATAC_Diff_result20210208/whfs-xs-190174_ATAC_Diff_result/数据可视化说明/YouCai.fa')

# 加载 IG 归因
attributions = np.load('attributions.npy')  # (500, 6000)
print(f'Attributions shape: {attributions.shape}')

# 加载 JASPAR motifs
motifs = parse_jaspar('JASPAR2024_CORE_plants_non-redundant_pfms_jaspar.txt')
print(f'JASPAR motifs: {len(motifs)}')

# 加载正样本坐标（前 150115 个，取测试集部分）
pos_coords = []
with open('/mnt/e/work/QT2_analysis/01_positive/positive_samples.bedpe') as f:
    for line in f:
        cols = line.strip().split('\t')
        pos_coords.append((cols[0], int(cols[1]), int(cols[2]), cols[3], int(cols[4]), int(cols[5])))

# 只取通过过滤的样本
# 用 IG 的样本索引（测试集正样本）
n_pos = 150115
test_start = int(n_pos * 0.8)
test_end = n_pos
np.random.seed(42)
sample_idx = np.random.choice(range(test_start, test_end), size=500, replace=False)

# PWM 打分函数
def pwm_score(seq, pwm_matrix):
    """用 PWM 给序列打分"""
    seq = seq.upper()
    nts = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    L = len(pwm_matrix[0])
    if len(seq) < L:
        return -999
    # 把 PWM 计数转成 log-odds
    total = np.array(pwm_matrix).sum(axis=1, keepdims=True)
    freq = (np.array(pwm_matrix) + 0.5) / (total + 2.0)
    log_odds = np.log2(freq / 0.25)
    score = 0
    for i, base in enumerate(seq[:L]):
        if base in nts:
            score += log_odds[nts[base], i]
    return score

# 对每个样本，找 IG 贡献最高的 20 bp 窗口
# 注意：IG 的 6000 bp 是 anchor1(3000) + anchor2(3000) 拼接
# 我们只看 anchor1 的 3000 bp（前 3000 列）
window_size = 20
top_motifs = []

for i, idx in enumerate(sample_idx):
    attr = attributions[i][:3000]  # anchor1 的前 3000 bp
    # 找滑动窗口里贡献最高的位置
    best_pos = 0
    best_score = -1
    for j in range(0, 3000 - window_size):
        s = attr[j:j+window_size].sum()
        if s > best_score:
            best_score = s
            best_pos = j

    # 从参考基因组提取这段序列
    chrom, start, end = pos_coords[idx][0], pos_coords[idx][1], pos_coords[idx][2]
    mid = (start + end) // 2
    seq_start = max(0, mid - 1500 + best_pos)
    seq_end = seq_start + window_size
    try:
        seq = str(genome[chrom][seq_start:seq_end])
    except Exception:
        continue

    # 和 JASPAR 比对
    best_motif = None
    best_motif_score = -999
    for mid_, m in motifs.items():
        sc = pwm_score(seq, m['matrix'])
        if sc > best_motif_score:
            best_motif_score = sc
            best_motif = (mid_, m['name'])

    if best_motif:
        top_motifs.append((i, best_motif[0], best_motif[1], best_motif_score, seq))

# 统计最常出现的 motif
from collections import Counter
motif_counts = Counter([t[2] for t in top_motifs])
print('\nTop 20 motifs:')
for name, count in motif_counts.most_common(20):
    print(f'{name}: {count}')

# 保存结果
with open('motif_matches.tsv', 'w') as f:
    f.write('sample_idx\tmotif_id\tmotif_name\tscore\tseq\n')
    for t in top_motifs:
        f.write(f'{t[0]}\t{t[1]}\t{t[2]}\t{t[3]:.3f}\t{t[4]}\n')

print(f'\nSaved {len(top_motifs)} matches to motif_matches.tsv')
