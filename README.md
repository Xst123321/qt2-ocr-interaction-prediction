# QT2 OCR Interaction Prediction

基于深度学习的甘蓝型油菜 QT2（N53-2）染色质开放区域（OCR）互作预测模型。

## 项目目标

- 利用 QT2 的 Hi-C 和 ATAC-seq 数据，构建 OCR 互作预测模型
- 验证模型预测的互作是否富集在活跃/抑制染色质区域
- 为油菜三维基因组调控网络研究提供方法学基础

## 数据来源

| 数据类型 | 来源 | 说明 |
|:---|:---|:---|
| Hi-C | 课题组 | QT2（N53-2），chr1-chr19 |
| ATAC-seq | 课题组 | QT2 种子时期，三个重复 |
| H3K27ac ChIP-seq | 课题组 | N53-2，两个重复 |
| H3K27me3 ChIP-seq | 课题组 | N53-2，两个重复 |
| 参考基因组 | 课题组 | YouCai.fa（chr1-chr19） |

## 流程概览

1. 从 Hi-C 数据提取显著互作（正样本）
2. 距离匹配采样构建负样本
3. 从 OCR 区域提取序列（中心 ±1500 bp）
4. 模型训练（CNN + Transformer）
5. 测试集评估
6. 用 H3K27ac/H3K27me3 做生物学验证

## 关键结果

- 训练集 216,732 / 验证集 30,962 / 测试集 61,924
- 验证 Accuracy：96.61%（最佳 96.87%）
- 测试集 AUC：0.9942，AUPR：0.9934
- 预测互作锚点显著富集在 H3K27ac（1.32 倍）和 H3K27me3（1.67 倍）区域

## 环境依赖

- WSL2 Ubuntu 22.04
- Python 3.11
- PyTorch 2.7.1 + CUDA 12.8
- scikit-learn、h5py、numpy
- bedtools 2.31.1

## 目录结构

- `data/`：数据来源和预处理记录
- `pipeline/`：正负样本构建、模型训练、验证步骤
- `results/`：结果汇总
- `assets/`：结果图
