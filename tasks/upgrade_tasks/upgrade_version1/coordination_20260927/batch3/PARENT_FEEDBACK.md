# 主进程复核反馈

继续完成本批全部任务，不削弱核心科学对照；在最终交付前核对以下具体问题。修改生成器及两个模式的产物、刷新manifest，并补正反例。前置输入阻塞是有效诊断而不是科学完成，不能强制虚构计算记录。

## batch3_all

Schema requires >=1 calculation and object record plus allocated_cores>=1 even for blocked-before-launch reports. Allow honest zero-engine diagnostic failures without fabricating a geometry or job. Successful density analysis currently forces energy; distinguish molecular jobs from analysis. Generic evidenced_collapse branch available on analysis/attribution/robustness rows; narrow it to meaningful physical candidate rows or explicitly prohibit using it for missing core comparisons.
