import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import csv

font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
try:
    fm.fontManager.addfont(font_path)
    matplotlib.rcParams['font.family'] = 'WenQuanYi Micro Hei'
except Exception:
    pass
matplotlib.rcParams['axes.unicode_minus'] = False

epochs, train_loss, train_acc, val_loss, val_acc = [], [], [], [], []
with open('/mnt/e/work/QT2_analysis/06_model/code/training_metrics.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        epochs.append(int(row['epoch']))
        train_loss.append(float(row['train_loss']))
        train_acc.append(float(row['train_acc']))
        val_loss.append(float(row['val_loss']))
        val_acc.append(float(row['val_acc']))

print(f'Total epochs: {len(epochs)}')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(epochs, train_loss, '-', label='Train loss', color='#4C72B0', linewidth=1.5)
ax1.plot(epochs, val_loss, '-', label='Val loss', color='#DD8452', linewidth=1.5)
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Loss', fontsize=12)
ax1.set_title('Training and Validation Loss', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_yscale('log')

ax2.plot(epochs, train_acc, '-', label='Train acc', color='#4C72B0', linewidth=1.5)
ax2.plot(epochs, val_acc, '-', label='Val acc', color='#DD8452', linewidth=1.5)
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Accuracy', fontsize=12)
ax2.set_title('Training and Validation Accuracy', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('training_curves.png', dpi=300)
print('Saved training_curves.png')
