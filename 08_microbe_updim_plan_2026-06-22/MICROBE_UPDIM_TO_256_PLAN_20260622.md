# 微生物侧特征升维与统一 256 维表征计划

## 1. 摘要

当前 Bio Vector R3 模型将反应、酶、底物和微生物四类对象统一投影到 256 维向量空间。反应、底物和酶在进入投影层前已经具有较高维度的原始表征：反应 DRFP 为 2048 维，底物 Morgan fingerprint 为 2048 维，酶 ESM-C 表征为 1152 维。相比之下，微生物侧当前仅使用 28 维人工汇总特征。

这一设置可以完成端到端训练，但存在明显的信息不平衡：微生物代谢网络本身包含大量代谢物、反应和核心网络连通性信息，而当前 28 维输入只保留了少量统计摘要。将 28 维直接映射到 256 维并不能增加真实生物学信息，反而可能使模型在正则化和对比学习压力下产生低维信号的过度展开。

本计划提出一个微生物侧 V2 表征方案：利用已完成的 RHEA core-preference target-level long CSV，将微生物-反应-代谢物层面的核心网络连通性信息展开为约 13.5k 至 13.8k 维的可解释稀疏特征，再通过归一化和投影网络统一降到 256 维。该方案保持与现有 R3 四模态统一向量空间兼容，同时显著提高微生物侧输入的信息量。

## 2. 当前维度不平衡问题

### 2.1 现有四模态输入与输出

R3 训练记录显示，全量训练样本为 145,607 条，四模态输入维度如下：

| 模态 | 当前输入来源 | 输入维度 | 统一输出维度 |
|---|---|---:|---:|
| 反应 | DRFP 反应指纹 | 2048 | 256 |
| 底物 | Morgan fingerprint | 2048 | 256 |
| 酶 | ESM-C pocket-pooled 表征 | 1152 | 256 |
| 微生物 | 人工汇总代谢特征 | 28 | 256 |

R3 最终输出文件中，四个模态的 embedding 均为 `(145607, 256)`，说明统一向量空间已经完成。但统一输出维度一致并不意味着输入信息量一致。对于反应、底物和酶，模型是在较高维原始表征基础上做降维和语义压缩；对于微生物，模型是在低维摘要基础上做扩展式投影。

### 2.2 当前 28 维微生物特征构成

当前微生物输入由三部分组成：

| 模块 | 维度 | 含义 |
|---|---:|---|
| core preference | 6 | 当前 RHEA 反应在对应微生物核心代谢网络中的连通性汇总 |
| cofactor stoichiometry | 16 | ATP、NAD、CoA、水、质子等常见辅因子/货币分子的化学计量系数 |
| main-metabolite coverage | 6 | 主反应物/主产物是否有可解释的 BiGG 映射 |

这 28 维特征能够描述“该反应在该微生物中是否容易接入核心代谢”，但它没有显式保留“具体是哪些代谢物接入了核心网络”“这些代谢物分别位于反应物侧还是产物侧”“不同 BigG 代谢物在不同微生物中的偏好差异”等信息。

### 2.3 为什么需要先升维再降维

反应、底物和酶的处理逻辑是从高维原始表征压缩到 256 维。微生物侧也应尽量先构建较完整的代谢特征，再学习到 256 维统一空间。

这里的“升维”不是简单地用神经网络把 28 维扩大到更高维，而是把已经存在但未使用的代谢网络信息显式展开。例如，将不同 BigG 代谢物作为不同特征维度，记录其在微生物核心网络中的连通状态。这样得到的高维特征具有明确生物学含义，随后再通过归一化、降维或投影网络压缩到 256 维。

## 3. Long CSV 数据来源与含义

### 3.1 数据产生时间与任务背景

RHEA core-preference full run 于 2026-05-25 在 HPC 上完成。该任务基于 2,867 个 CarveMe 微生物代谢模型的 NIS Core 结果，分析 RHEA 反应中的代谢物能否接入对应微生物的核心代谢网络。

相关数据随后在 2026-06-02 被整理为 microbe long-preference add-on，并与 clean training package 对齐。该 add-on 不替代主训练包，而是补充了更细粒度的 target-level 代谢偏好结果。

### 3.2 分析方法

每个微生物可以理解为一个代谢网络。NIS Core 提取的核心代谢网络主要覆盖糖酵解、磷酸戊糖途径、TCA 循环和丙酮酸代谢等中心代谢模块。RHEA 反应被临时接入该网络后，分析程序对反应中的每个可识别 BigG 代谢物进行连通性判断：

| 判断结果 | 含义 | 生物学解释 |
|---|---|---|
| `in_core` | target 代谢物本身已在核心网络中 | 与中心代谢高度相关 |
| `reachable` | target 代谢物不在核心中，但可通过网络路径到达核心代谢物 | 可能被该微生物代谢网络接纳 |
| `not_reachable` | 在设定搜索深度内无法到达核心网络 | 可能是孤立或远离核心代谢的代谢物 |

这里的 target 代谢物指 RHEA 反应中具有明确 BigG ID 的代谢物。BigG ID 是代谢模型中常用的标准化代谢物标识，例如 `atp_c` 表示细胞质中的 ATP，`glu__L_c` 表示细胞质中的 L-谷氨酸。

### 3.3 Long CSV 的行粒度

Long CSV 的每一行对应一个三元组：

```text
微生物模型 × RHEA 反应 × target BigG 代谢物
```

核心字段包括：

| 字段 | 含义 |
|---|---|
| `assembly_accession` | 微生物基因组/模型标识 |
| `rhea_ids` | RHEA 反应编号 |
| `CANO_RXN_SMILES` | 标准化反应 SMILES |
| `target_bigg_met_id` | 当前分析的具体 BigG 代谢物 |
| `target_met_role` | 该代谢物在反应中是反应物、产物还是零净变化项 |
| `target_met_in_original_model` | 该代谢物是否已存在于原始微生物模型中 |
| `target_met_in_core` | 该代谢物是否在 NIS Core 网络中 |
| `min_path_length` | 到核心网络的最短路径长度；0 表示本身在核心中，-1 表示不可达 |
| `preference_score` | 连通性得分，当前结果中可达为 1，不可达为 0 |
| `preference_status` | `in_core`、`reachable` 或 `not_reachable` |

因此，Long CSV 不是简单的标签表，而是保留了具体代谢物身份、反应角色和网络连通性的细粒度证据。

## 4. 已完成统计结果

### 4.1 主训练包与 long add-on 规模

基于本地 clean training package 和 microbe long-preference add-on 的审计结果：

| 数据项 | 数量 |
|---|---:|
| clean training examples | 145,607 |
| unique assembly_accession | 2,475 |
| microbe_features.jsonl 行数 | 145,607 |
| long CSV shard 数 | 20 |
| long target-level 行数 | 692,151 |
| long unique reaction-model keys | 175,242 |
| long unique target BigG metabolite IDs | 1,154 |

其中 clean training examples 是当前 R3 实际训练样本；long CSV 的 692,151 行覆盖更完整的候选反应-微生物组合，其中与 clean training examples 对齐后，可展开为 629,691 条 example-target 记录。

### 4.2 当前 28 维特征的信息压缩程度

当前 `connectable_target_ratio` 只有 5 个不同取值，且均值为 0.9562。这说明当前特征对“是否可连通”高度概括，但分辨率较低。

核心类别分布如下：

| 类别 | 数量 | 比例 |
|---|---:|---:|
| all_targets_connectable | 137,565 | 94.48% |
| no_targets_connectable | 6,021 | 4.14% |
| partial_connectable | 2,021 | 1.39% |

这类汇总特征适合做粗粒度判断，但不适合表达“哪类代谢物在哪些微生物中更可利用”的细粒度差异。

### 4.3 可展开的高维信息量

基于已有表格，可以构建以下候选矩阵：

| 候选矩阵 | 行数 | 维度 | 非零列数 | 含义 |
|---|---:|---:|---:|---|
| current_28_engineered | 145,607 | 28 | 28 | 当前 R3 微生物输入 |
| stoich_bigg_signed | 145,607 | 1,122 | 1,116 | BigG 代谢物的净化学计量系数 |
| stoich_bigg_role_split | 145,607 | 2,244 | 1,852 | 分开记录反应物侧和产物侧 BigG 代谢物 |
| long_target_x_9_channels | 145,607 | 10,386 | 6,332 | target BigG 代谢物 × 连通性/角色通道 |
| combined_big_v2_candidate | 145,607 | 13,780 | 9,328 | BigG-only V2 合并候选 |

如果去掉 20 个低信息量的通用代谢物或辅因子，例如水、质子、ATP、ADP、NADH、CO2、Pi 等，合并候选仍有约 13,540 维。这说明微生物侧升维不是人为扩展，而是来自已存在的可解释代谢网络信息。

### 4.4 归一化的必要性

未归一化的高维矩阵会被高频通用代谢物主导，例如 `h_c`、`h2o_c`、`atp_c` 等。这些代谢物几乎出现在许多反应中，能够造成统计上的强信号，但其生物学特异性较弱。

矩阵审计显示：

| 矩阵 | top-k energy / Frobenius | top-k effective rank | 解释 |
|---|---:|---:|---|
| combined_big_v2_candidate，未归一化 | 0.9004 | 4.20 | 高频通用特征占主导 |
| combined_big_v2_candidate，列 L2 归一化 | 0.0667 | 46.25 | 频率支配明显减弱，更多维度参与表达 |

因此，V2 微生物特征不能直接把原始稀疏计数喂入模型。必须进行列归一化、分块缩放或低信息代谢物降权，否则模型主要学习到的是“常见分子是否出现”，而不是微生物代谢偏好。

## 5. 拟采用的升维方案

### 5.1 主方案：BigG-only 可解释特征

首版 V2 建议只使用明确 BigG 身份的代谢物作为高维特征主体。理由如下：

1. BigG ID 与 CarveMe 模型和代谢网络直接兼容，具有明确代谢物身份。
2. BigG 特征可解释性强，可以追溯到具体代谢物。
3. 相比 placeholder，BigG 特征更适合作为正式训练输入和结果解释基础。

Placeholder 代谢物仍可保留在附录分析或消融实验中，但不建议进入首版主模型。Placeholder 是为无法可靠映射到 BiGG 的 RHEA 代谢物生成的临时 ID，它可以帮助构建反应网络，但其生物学身份不如 BigG 明确。

### 5.2 特征模块设计

V2 微生物输入建议包含四个模块：

| 模块 | 预计维度 | 说明 |
|---|---:|---|
| 当前 28 维基础特征 | 28 | 保留 R3 已使用的核心汇总信息 |
| BigG signed stoichiometry | 1,122 | 每个 BigG 代谢物的净化学计量系数 |
| BigG role-split stoichiometry | 2,244 | 分开记录反应物侧消耗和产物侧生成 |
| Long target preference channels | 10,386 | 每个 target BigG 代谢物的出现、连通状态、反应角色和模型存在性 |

合并后约 13,780 维；去除常见低信息代谢物后约 13,540 维。

Long target preference channels 建议使用以下 9 个通道：

| 通道 | 含义 |
|---|---|
| present_count | 该 target 代谢物是否在当前微生物-反应组合中出现 |
| preference_score_sum | 连通性得分 |
| status_in_core | 是否已在核心网络中 |
| status_reachable | 是否可到达核心网络 |
| status_not_reachable | 是否不可达 |
| role_reactant | 是否位于反应物侧 |
| role_product | 是否位于产物侧 |
| role_zero_net | 是否为零净变化项 |
| target_in_original_model | 是否已存在于原始 CarveMe 模型 |

### 5.3 归一化与低信息代谢物处理

建议采用以下预处理策略：

1. 对每个特征列做 L2 归一化或标准化，避免高频特征支配训练。
2. 对不同模块做分块缩放，使 28 维基础特征、stoichiometry 特征和 long target 特征的整体量级可比。
3. 对水、质子、ATP、ADP、NAD、NADH、CO2、Pi、PPi 等通用代谢物进行降权或过滤。
4. 保留过滤前和过滤后的统计结果，用于后续消融比较。

低信息代谢物并非错误数据。它们在代谢网络中非常重要，但在区分微生物对特定底物的代谢偏好时信息量较低。如果不做降权，这些代谢物容易成为模型的主导信号。

## 6. 拟采用的降维方案

### 6.1 与现有 R3 投影结构保持兼容

现有 R3 模型中，反应、酶和底物均通过多层投影器映射到 256 维，典型结构为：

```text
input_dim → Linear(512) → BatchNorm → ReLU → Linear(512) → BatchNorm → ReLU → Linear(256) → L2 normalize
```

微生物侧当前也输出 256 维 embedding，并通过对比学习与酶、底物等模态对齐。V2 方案应保持最终输出仍为 256 维，以兼容现有检索、FAISS/NN index、metadata 和下游 agent 接口。

### 6.2 推荐路线

首版建议采用如下路线：

```text
13.5k-13.8k sparse BigG microbe features
→ column normalization / block scaling
→ sparse or dense projection to 512 hidden dimension
→ microbe head projection to 256
→ L2 normalization
```

如果训练资源或稀疏矩阵支持有限，也可以采用两阶段降维：

```text
13.5k sparse features
→ Truncated SVD / PCA to 512 or 1024
→ existing microbe projector
→ 256 unified embedding
```

两种路线的科学目标一致：先保留更多可解释代谢信息，再学习与其他模态对齐的 256 维微生物表征。

### 6.3 不建议的路线

不建议直接将当前 28 维输入通过更大的 MLP 扩展到 512 或 1024 维后再降到 256。这样只会改变模型容量，而不会增加真实输入信息。微生物侧的关键改进应来自代谢网络信息的显式展开，而不是对原 28 维摘要的数学扩张。

## 7. 执行步骤

### 7.1 数据构建

1. 读取 clean training package 中的 145,607 条训练样本。
2. 使用 `example_id` 和 `(assembly_accession, CANO_RXN_SMILES, rhea_ids)` 将主训练样本与 long preference add-on 对齐。
3. 构建 BigG 代谢物词表：
   - stoichiometry BigG IDs：1,122 个。
   - long target BigG IDs：1,154 个。
4. 生成 V2 稀疏特征矩阵：
   - 当前 28 维基础特征。
   - stoich signed 特征。
   - stoich role-split 特征。
   - long target × 9 channels 特征。
5. 生成特征字典和审计文件，记录每一维对应的代谢物或统计含义。

### 7.2 预处理

1. 对每个特征列做归一化，优先采用列 L2 归一化。
2. 对不同模块进行分块缩放，避免某一模块主导训练。
3. 生成两套候选矩阵：
   - 全 BigG 特征版本。
   - 过滤/降权低信息代谢物版本。
4. 对两个版本分别记录稀疏度、非零列数、行非零分布和近似谱统计。

### 7.3 模型接入

1. 将微生物输入维度从 28 调整为 V2 特征维度或 SVD 后维度。
2. 保持最终 microbe embedding 输出为 256 维。
3. 保留 concept anchor 监督，但需要根据 V2 特征重新审查 anchor 目标是否仍合理。
4. 先进行 smoke test，再进行 300 样本或小规模训练，最后进入全量训练。

### 7.4 对照实验

建议至少进行以下对照：

| 实验 | 微生物输入 | 目的 |
|---|---|---|
| R3 baseline | 当前 28 维 | 当前基线 |
| V2-A | 28 维 + BigG stoich | 检查具体代谢物身份是否改善 |
| V2-B | 28 维 + long target channels | 检查 target-level core preference 的贡献 |
| V2-C | BigG combined full | 检查完整 BigG-only 高维特征效果 |
| V2-D | BigG combined + low-info filtering | 检查低信息代谢物过滤是否提升泛化 |

主要评估指标包括 E→M、S→M 检索指标，microbe embedding 有效秩，低信息代谢物主导程度，以及 R→E 主任务是否受到负面影响。

## 8. 可能风险与应对

### 8.1 高频通用代谢物支配模型

风险：水、质子、ATP、ADP 等代谢物出现频率高，可能让模型学习到通用代谢网络结构，而非特定底物偏好。

应对：列归一化、模块缩放、低信息代谢物过滤或降权，并做消融实验。

### 8.2 Placeholder 解释性不足

风险：placeholder 不是标准代谢物身份，直接用于主模型可能降低解释可信度。

应对：首版主方案仅使用 BigG 特征。Placeholder 只用于附录统计、错误分析或后续消融。

### 8.3 Row-level 特征与 microbe-level 特征混合

当前 V2 特征仍主要描述“微生物-反应”组合，而不是纯粹的“微生物本体”。这适合当前训练数据结构，但如果后续要做宿主菌推荐或跨反应泛化，可能需要进一步构建 assembly-level 微生物代谢画像。

应对：首版先保持与 R3 训练样本粒度一致；后续可聚合到 assembly-level，形成每个微生物的整体代谢能力向量。

### 8.4 维度升高带来训练成本增加

风险：13k 维稀疏输入如果直接转为 dense，显存和训练时间会增加。

应对：优先使用稀疏矩阵存储和分批加载；必要时先用 Truncated SVD/PCA 降到 512 或 1024，再进入现有 projector。

### 8.5 与现有 R3 结果不可直接比较

风险：更换微生物输入后，E→M 和 S→M 指标可能变化，不能直接视为单一因素变化。

应对：使用严格对照实验，只改变微生物输入，保持反应、酶、底物特征和训练参数尽量一致。

## 9. 需要进一步确认的内容

1. 是否认可 BigG-only 作为首版 V2 微生物特征主方案。
2. 低信息代谢物是过滤、降权，还是保留并通过归一化控制。
3. Placeholder 是否完全排除在主训练外，或作为附加消融实验。
4. 首版目标是改进 row-level 微生物-反应匹配，还是同步构建 assembly-level 微生物本体画像。
5. 降维路线优先选择端到端 projector，还是先 SVD/PCA 到中间维度再训练。

## 10. 预期产出

如果该方案通过，后续应形成以下产物：

| 产物 | 内容 |
|---|---|
| `microbe_v2_feature_matrix.npz` | V2 微生物稀疏或降维后特征矩阵 |
| `microbe_v2_feature_vocab.json` | 每一维特征对应的代谢物、通道和解释 |
| `microbe_v2_feature_audit.md` | 特征构建审计、稀疏度、归一化和低信息代谢物统计 |
| V2 训练脚本或配置 | 接入新的微生物输入维度，输出仍为 256 维 |
| V2 对照实验结果 | R3 baseline 与 V2-A/B/C/D 的指标比较 |

## 11. 结论

微生物侧当前的主要瓶颈不是最终 256 维输出，而是输入信息量过低。现有 long preference add-on 已经包含大量未被 R3 微生物分支充分利用的代谢网络信息。基于 BigG 代谢物身份、反应角色和核心网络连通性，可以将微生物侧输入从 28 维提升到约 13.5k 至 13.8k 维的可解释稀疏特征，再通过归一化和投影网络统一降到 256 维。

该方案与现有 R3 四模态统一向量空间兼容，并且能够把微生物表征从“少量连通性摘要”提升为“具体代谢物层面的代谢偏好画像”。首版建议采用 BigG-only 主方案，谨慎处理低信息通用代谢物，并将 placeholder 保留为后续消融或补充分析。

