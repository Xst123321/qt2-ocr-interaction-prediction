# 数据来源

本项目使用的数据全部由课题组提供，参考基因组为 `YouCai.fa`（chr1-chr19）。

## 1. Hi-C 数据（QT2 / N53-2）

位置：`/mnt/e/group_data/hi-c/02.Hi-C attachment/result/QT2/`

关键文件：

- `04.显著互作分析/cis_interaction.annotation.txt`：cis 互作（159,675 个）
- `04.显著互作分析/cis_interaction_10000.txt`：10 kb 分辨率互作矩阵
- `00.数据过滤及比对/QT2-1.align.statistics`：比对统计
- `01.互作矩阵及互作图/`：接触矩阵

## 2. ATAC-seq 数据（QT2）

位置：`/mnt/e/group_data/atac/whfs-xs-190174_ATAC_Diff_result20210208/`

关键文件：

- `01.QualityControl/QT-2-1/QT-2-1_peaks.narrowPeak`
- `01.QualityControl/QT-2-2/QT-2-2_peaks.narrowPeak`
- `01.QualityControl/QT-2-3/QT-2-3_peaks.narrowPeak`

合并后得到 120,324 个 OCR 区域。

## 3. ChIP-seq 数据（N53-2）

H3K27ac：

- `N53-2_H3K27ac_1_peaks.narrowPeak`
- `N53-2_H3K27ac_2_peaks.narrowPeak`

H3K27me3：

- `N53-2_H3K27me3_1_peaks.broadPeak`
- `N53-2_H3K27me3_2_peaks.broadPeak`

## 4. 参考基因组

位置：`/mnt/e/group_data/atac/whfs-xs-190174_ATAC_Diff_result20210208/whfs-xs-190174_ATAC_Diff_result/数据可视化说明/YouCai.fa`

染色体命名：`chr1`–`chr19`
