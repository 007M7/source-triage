# Attention Budget Screen v0.1 合并工程实现文件

日期：2026-07-15

状态：已实现、已验收、已发布

## 1. 合并决策

将原有两个独立能力合并为一个主工作流 Skill：

```text
content-signal-screen：内容质量 / 疑似 Slop 风险
source-triage：原始注意力预算决策
          ↓
attention-budget-screen：统一工作流入口
```

新主载体：

```text
https://github.com/007M7/attention-budget-screen
```

旧仓库保留兼容性和历史实现，不删除、不改变原有核心契约。

## 2. 产品叙事

统一主题：

> Slop 洪水里，先识别信息污染，再决定把注意力花在哪里。

对外解释为两个连续问题：

1. 这段内容有没有值得处理的信息？
2. 它现在值得占用我的时间和认知资源吗？

核心叙事不是“AI 帮你读更多”，而是“在注意力被消耗之前，先判断内容和投入是否值得”。

## 3. 工作流契约

### 3.1 `full_workflow`

默认模式：

```text
内容质量 / Slop 四信号筛查
        ↓
原始注意力预算决策
        ↓
下一步建议
```

`workflow_decision` 必须等于注意力阶段的 `triage_decision`。

### 3.2 `content_quality_only`

只回答内容是否存在疑似 Slop 风险。注意力阶段为 `not_run`，最终决策为 `quality_screen_only`。

### 3.3 `attention_only`

兼容原 Source Triage。内容阶段为 `not_run`，最终决策等于注意力阶段的 `triage_decision`。

## 4. 两阶段边界

### 内容阶段

四个信号：

- `concrete_takeaway`：具体收获；
- `source_specificity`：来源具体性；
- `author_footprint`：作者痕迹；
- `cognitive_progress`：认知推进。

风险等级：`low`、`medium`、`high`、`indeterminate`。

### 注意力阶段

保留 Source Triage 的决策枚举：

- `quick_read_now`；
- `read_deep_now`；
- `project_relevant_but_not_now`；
- `reference_only`；
- `defer_or_monitor`；
- `do_not_invest_further_now`；
- `pending_context`。

### 合并规则

- `slop_risk=high` 只进入注意力阶段的 basis，不自动转换为跳过。
- `slop_risk=low` 也不证明来源与当前项目相关或值得深读。
- 内容阶段 `indeterminate` 时，只要标题、摘要、目录和用户目标足够，注意力阶段仍可运行。
- 注意力阶段 `pending_context` 时，不得用 Slop 风险代替用户目标。
- 两个阶段必须分别记录 inspected sections、uncertainty 和 not_inferred。

## 5. 输入与输出

主输出 schema：

```text
schema_version: 0.1
mode: full_workflow | content_quality_only | attention_only
workflow_decision:
content_quality:
attention_gate:
uncertainty:
not_inferred:
recommended_next_gate:
writeback_status: none
```

`content_quality` 和 `attention_gate` 均有显式 `status`，允许 `evaluated`、`indeterminate`、`not_run`。

## 6. 实现与验收范围

- 标准 `SKILL.md` 与 frontmatter；
- `agents/openai.yaml`；
- 工作流规则和输出模板；
- 机械 validator；
- 三种模式示例；
- 8 个 validator 单元测试；
- 24 条行为评测：8 full_workflow、4 content_quality_only、4 attention_only、4 edge_case、4 neighbor_confusion；
- 中文 README、Codex/Claude Code 接入说明、MIT License、隐私边界；
- 独立前向测试。

## 7. 兼容与迁移

旧项目：

- `source-triage`：保留注意力决策旧入口；README 推荐统一 Skill。
- `content-signal-screen`：保留内容质量旧入口；README 推荐统一 Skill。

新用户优先安装：

```text
https://github.com/007M7/attention-budget-screen
```

不在旧 Skill 中偷偷增加新的合并输出，避免破坏旧用户已有契约。

## 8. 已知边界

- 不检测 AI 作者身份；
- 不做事实核验；
- 不判断作者动机；
- 不做医学、法律或学术认证；
- 不自动删除、屏蔽、上传、发布或写入记忆；
- 不宣称准确率、节省时间或长期行为改变已经被证明。

## 9. 当前状态

```text
engineering_spec_written: true
implemented: true
validated: true
forward_tested: true
published: true
remote_content_verified: pending_final_audit
effect_proven: false
```
