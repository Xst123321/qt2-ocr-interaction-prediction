# 正负样本构建

## 1. 正样本（Hi-C 显著互作）

从 QT2 的 cis_interaction.annotation.txt 提取互作对，转换为 BEDPE 格式：

```bash
cd /mnt/e/work/QT2_analysis

awk -F'\t' '{
    split($2, a, ":");
    split(a[2], b1, "-");
    split($3, c, ":");
    split(c[2], b2, "-");
    print a[1]"\t"b1[1]"\t"b1[2]"\t"c[1]"\t"b2[1]"\t"b2[2]"\t1"
}' "/mnt/e/group_data/hi-c/02.Hi-C attachment/result/QT2/04.显著互作分析/cis_interaction.annotation.txt" > 01_positive/positive_samples.bedpe

wc -l 01_positive/positive_samples.bedpe

结果：159,675 个正样本。

## 2. 负样本（距离匹配采样）

负样本需要和正样本的距离分布匹配，避免模型只学"距离近就互作"。

正样本距离分布：

| 距离区间 | 正样本数量 | 占比 |
|:---|:---|:---|
| 0-100 kb | 43,582 | 27.3% | 
| 100 kb-1 Mb | 32582 | 20.4% |
| 1-10 Mb | 45,107 | 28.2% |
| 10-60 Mb | 38,404 | 24.1% |

负样本生成：

- 0-100 kb：用 bedtools window -w 100000 从 OCR 区域找近距离对
- 100 kb-1 Mb：用 bedtools window -w 1000000 找中等距离对
- 1-10 Mb 和 10-60 Mb：从 OCR 区域随机组合，筛选目标距离范围

最终负样本：159,954 个。

## 3. 锚点与 OCR 重叠验证

用 bedtools intersect 检查 Hi-C 锚点是否落在 OCR 区域上：

- anchor1 落在 OCR 上：120,223 / 159,675 = 75.3%
- anchor2 落在 OCR 上：120,865 / 159,675 = 75.7%

结果验证了"Hi-C 互作锚点位于开放染色质区域"这一核心假设。
