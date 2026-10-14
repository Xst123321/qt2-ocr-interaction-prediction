# 模型训练与评估

## 1. 序列提取

从参考基因组 YouCai.fa 提取每个锚点中心 ±1500 bp 的序列（共 3000 bp），One-hot 编码为 (4, 3000) 数组。过滤 N 含量 > 50% 的样本。

- 正样本：159,675 → 150,115（过滤 6.0%）
- 负样本：159,954 → 159,503（过滤 0.3%）

## 2. 数据存储

为避免内存溢出，数据存为 .npy 格式，用 np.load(..., mmap_mode='r') 按需读取。

- anchor1.npy：14 GB
- anchor2.npy：14 GB
- labels.npy：2.4 MB

## 3. 模型架构

参考 PlantCTCIP 的 CNN + Transformer 架构：

- CNN 模块：6 层卷积，通道数 1→64→128→256→128→64→4
- Transformer 模块：6 层编码器，4 头注意力，d_model=4，dim_feedforward=8
- 分类头：全连接层 + Dropout(0.3)，输出 2 类

## 4. 训练配置

- 训练集：216,732（70%）
- 验证集：30,962（10%）
- 测试集：61,924（20%）
- batch_size：64
- optimizer：Adam，lr=1e-4
- loss：CrossEntropyLoss
- epoch：180

## 5. 训练结果

| 指标 | 数值 |
|:---|:---|
| 训练 Acc | 99.90% |
| 验证 Acc | 96.61% |
| 最佳验证 Acc | 96.87%（第 148 epoch） |

每 5 个 epoch 保存一次 checkpoint，支持断点续跑。

## 6. 测试集评估

| 指标 | 数值 |
|:---|:---|
| AUC | 0.9942 |
| AUPR | 0.9934 |
| Precision | 95.84% |
| Recall | 97.55% |
| F1 | 96.69% |
