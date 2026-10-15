import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import logomaker
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '/mnt/e/work/qt2-ocr-interaction-prediction/analysis/motif')
from parse_jaspar import parse_jaspar

font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
try:
    fm.fontManager.addfont(font_path)
    matplotlib.rcParams['font.family'] = 'WenQuanYi Micro Hei'
except Exception:
    pass

motifs = parse_jaspar('JASPAR2024_CORE_plants_non-redundant_pfms_jaspar.txt')

top_motifs = ['CRF3', 'DOF3.1', 'ERF069', 'Dof3', 'DOF5.6', 'AZF2']

name_to_id = {}
for mid, m in motifs.items():
    name_to_id[m['name']] = mid

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for i, name in enumerate(top_motifs):
    if name not in name_to_id:
        continue
    mid = name_to_id[name]
    matrix = np.array(motifs[mid]['matrix'])
    matrix = matrix / matrix.sum(axis=0, keepdims=True)

    # 转成 DataFrame，列名是 A/C/G/T
    df = pd.DataFrame(matrix.T, columns=['A', 'C', 'G', 'T'])

    # 转成 information
    info_df = logomaker.transform_matrix(
        df,
        from_type='probability',
        to_type='information'
    )

    logomaker.Logo(info_df, ax=axes[i], color_scheme='classic')
    axes[i].set_title(f'{name} ({mid})', fontsize=12, fontweight='bold')
    axes[i].set_ylabel('Information (bits)', fontsize=10)

plt.tight_layout()
plt.savefig('motif_logos.png', dpi=300)
print('Saved motif_logos.png')
