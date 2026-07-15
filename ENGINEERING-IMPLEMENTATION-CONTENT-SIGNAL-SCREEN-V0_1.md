# Content Signal Screen v0.1 工程实现文件

状态：设计冻结前评审稿

日期：2026-07-15

所属产品族：Source Triage 邻接能力

当前仓库：`https://github.com/007M7/source-triage`

## 0. 执行结论

本任务实现一个独立的内容质量风险筛查 Skill，暂定产品名为 **Content Signal Screen**，对外叙事可使用“Slop 四信号筛查”。

它不修改 `source-triage` 当前的注意力决策契约，不增加新的 `triage_decision` 枚举，也不把“疑似低信息量”自动转换为“现在不值得读”。

第一阶段建议采用独立 Skill 包形态。当前 `source-triage` 仓库保留为 Source Triage 主 Skill；新能力通过独立载体发布，验收后再在 Source Triage README 中增加邻接项目链接。

本文件是工程实现与验收依据，不代表代码已经实现，也不代表 GitHub 已经发布。

## 1. 问题定义

### 1.1 用户问题

用户面对文章、帖子、AI 生成内容或批量内容时，常见的前置问题不是“它是不是 AI 写的”，而是：

```text
这段内容是否可能只是低投入、低信息量、为算法和流量生产的内容？
```

用户需要的是一个低成本、可解释、能主动承认不确定性的筛查，而不是一个声称识别真伪或识别 AI 作者的分类器。

### 1.2 目标

在正文或足够样本可用时，基于四个信号输出“疑似内容污染风险”及证据：

1. 具体收获；
2. 来源具体性；
3. 作者不可替代痕迹；
4. 认知推进而非单纯情绪刺激。

### 1.3 非目标

本版本不做以下事情：

- 不判断内容是否由 AI 生成；
- 不判断内容是否事实为真；
- 不判断作者是否恶意、懒惰或在欺骗用户；
- 不给出“这篇内容一定没有价值”的结论；
- 不替代 `source-triage` 的阅读注意力决策；
- 不自动抓取网页、上传来源、调用外部搜索或建立遥测；
- 不自动修改 `source-triage`、Founder-Agent OS 或任何长期记忆；
- 不因筛查结果自动删除、屏蔽、转发或发布内容。

## 2. 产品边界与邻接关系

### 2.1 两个 Skill 的职责

| 能力 | 主要问题 | 典型输出 |
|---|---|---|
| `source-triage` | 这份来源现在值得占用多少注意力？ | 跳过、延后、参考、快读、深读 |
| `content-signal-screen` | 这段内容是否存在低投入/低信息量/批量化风险？ | 风险等级、四信号、证据、不确定性 |

两者可以串联，但 v0.1 不自动串联：

```text
内容样本
   ↓（用户明确要求时）
Content Signal Screen：内容质量风险筛查
   ↓（用户另行询问时）
Source Triage：注意力预算决策
```

### 2.2 邻居混淆规则

以下输入默认触发 `source-triage`，不触发本 Skill：

```text
这篇文章值得我现在读吗？
这份报告和我的项目相关吗？
我只有 10 分钟，应该看哪些部分？
```

以下输入才触发本 Skill：

```text
这篇内容是不是信息垃圾？
这段内容是否疑似 slop？
这批 AI 文章是否只是批量内容？
帮我在发布前检查这段内容的信息质量风险。
```

如果用户同时询问两件事，应分两个阶段回答，不得把 `slop_risk=high` 直接映射为 `do_not_invest_further_now`。

## 3. 名称与载体决策

### 3.1 内部能力名

```text
content-signal-screen
```

选择中性名称的原因：

- “slop”适合产品传播，但不应被实现层当作事实标签；
- 中性名称允许未来覆盖低信息量内容、内容农场、模板化营销文案等邻接现象；
- 能降低用户把它误解为 AI 检测器或内容审查器的风险。

### 3.2 建议公开仓库

建议单独建立：

```text
https://github.com/007M7/content-signal-screen
```

不建议将第二个 `SKILL.md` 直接放入 `source-triage` 根目录的子目录后宣称可直接安装。当前 Skill 载体以“一个目录对应一个 Skill”为标准，独立仓库才能保持 Codex / Claude Code 接入路径清晰。

### 3.3 与现有仓库的同步关系

实施完成后，GitHub 同步分两部分：

1. 新建并发布 `content-signal-screen` 独立仓库；
2. 在 `source-triage` 的 README“邻接能力/未来方向”中增加经过验收的新仓库链接。

在新能力未通过验收前，不修改 Source Triage 的核心行为描述，不提前把候选链接写成已发布能力。

## 4. v0.1 输入契约

### 4.1 最小输入

至少需要以下之一：

- 可读取的正文；
- 足够判断的正文样本；
- 用户提供的多个内容片段。

仅有标题、封面、账号名或“它是不是 AI 写的”时，应返回 `indeterminate`，并说明无法负责地判断。

### 4.2 输入字段建议

```json
{
  "schema_version": "0.1",
  "source": {
    "title": "",
    "path_or_url": "",
    "source_type": "article|post|video_transcript|report|other",
    "sensitivity": "public|private|unknown"
  },
  "content_sample": "",
  "user_question": "",
  "context": "optional"
}
```

约束：

- `content_sample` 不是自动上传字段；由用户主动提供或本地运行时读取；
- 不把完整原文写入公开候选、测试仓库或遥测；
- `context` 只用于解释用户需求，不用于推断作者意图。

## 5. 输出契约

### 5.1 核心输出

```json
{
  "schema_version": "0.1",
  "run_id": "optional-local-id",
  "created_at": "2026-07-15T00:00:00Z",
  "slop_risk": "low|medium|high|indeterminate",
  "basis": "",
  "input_coverage": "metadata_only|sampled_content|full_content|other",
  "inspected_sections": [],
  "signals": {
    "concrete_takeaway": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    },
    "source_specificity": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    },
    "author_footprint": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    },
    "cognitive_progress": {
      "rating": "strong|mixed|weak|unknown",
      "evidence": "",
      "confidence": "low|medium|high"
    }
  },
  "uncertainty": "",
  "not_inferred": "",
  "recommended_next_gate": "",
  "writeback_status": "none"
}
```

### 5.2 风险等级语义

- `low`：四个信号大体显示出具体内容、来源或作者投入；不代表事实已经核验。
- `medium`：信号混合，存在部分低信息量风险，但证据不足以作强判断。
- `high`：多个信号同时偏弱，且样本足够；仍只能表述为“疑似风险较高”。
- `indeterminate`：正文不足、内容类型特殊或信号冲突，系统应主动停止强判断。

### 5.3 必须保留的否定边界

每次输出都必须明确：

- AI 参与生产不等于 slop；
- 疑似 slop 不等于事实错误；
- 疑似 slop 不等于不值得阅读；
- 本次结果不是作者动机判断；
- 本次结果不是专业事实、法律、医疗或学术结论。

## 6. 四信号实现规则

### 6.1 `concrete_takeaway`

检查内容能否让读者复述至少一个具体的概念、事实、数据、案例、方法或可检验观点。

判定提示：

- `strong`：能够定位多个具体认知增量；
- `mixed`：有少量具体内容，但大量套话或重复；
- `weak`：读完只剩情绪和模糊印象；
- `unknown`：正文样本不足。

禁止：把“内容简单”直接判为弱；面向初学者的简洁解释仍可能有价值。

### 6.2 `source_specificity`

检查是否出现可定位的人、研究、数据、原始链接、案例、时间或可复核材料。

判定提示：

- `strong`：来源可定位且与论断对应；
- `mixed`：有部分来源，但关键结论仍模糊；
- `weak`：大量使用“专家认为”“研究表明”但不提供定位；
- `unknown`：内容类型本身不要求外部来源，或样本不足。

禁止：把所有个人经验、诗歌或观点表达都按学术论文标准扣分。

### 6.3 `author_footprint`

检查是否存在具体经历、独特判断、责任承诺、过程细节或与作者身份绑定的内容。

判定提示：

- `strong`：替换账号或作者后，内容明显不再成立；
- `mixed`：部分内容有作者痕迹，部分内容是通用模板；
- `weak`：换号后可以原样发布；
- `unknown`：匿名内容、转述内容或样本不足。

禁止：因匿名就推断内容低质；匿名是证据缺失，不是负面事实。

### 6.4 `cognitive_progress`

检查内容是否减少不确定性、提供新角度、解释因果或提出可检验的判断，而不只是刺激感动、愤怒、惊奇或焦虑。

判定提示：

- `strong`：读者获得可复述的新理解或下一步问题；
- `mixed`：情绪表达和认知推进并存；
- `weak`：主要刺激情绪，没有可识别的认知增量；
- `unknown`：内容是纯娱乐、艺术或样本不足。

禁止：把情绪表达本身判为无价值；情绪内容可能具有文化、社交或审美价值。

## 7. 风险聚合规则

### 7.1 v0.1 不使用数学评分

v0.1 不输出伪精确分数，不把四个信号加权成百分比。原因：

- 当前没有人工标注集证明权重；
- 四个信号不是独立变量；
- 不同内容类型的“来源”和“作者痕迹”要求不同；
- 精确数字会诱导用户误读为经过科学校准的检测器。

### 7.2 允许的聚合表达

只有在以下条件同时满足时，才允许输出 `high`：

1. 输入覆盖足够；
2. 至少三个信号为 `weak`；
3. 没有明显的内容类型例外；
4. 输出列出每个弱信号对应的证据；
5. 明确声明这只是疑似风险。

否则优先使用 `medium` 或 `indeterminate`。

## 8. 执行流程

### Phase 0：触发与边界

完成标准：确认用户询问的是内容质量风险，而不是阅读注意力、事实核验或作者身份。

### Phase 1：输入覆盖检查

完成标准：记录来源类型、实际读取的正文范围和是否足以判断；不足时直接允许 `indeterminate`。

### Phase 2：四信号分析

完成标准：每个信号都有 rating、证据和 confidence；不得省略未知项。

### Phase 3：风险聚合

完成标准：输出一个风险等级，不输出多个互相竞争的最终标签；高风险必须满足第 7.2 节条件。

### Phase 4：边界回显

完成标准：输出 `uncertainty`、`not_inferred` 和 `recommended_next_gate`。

### Phase 5：停止

完成标准：返回筛查结果后停止；不自动调用 `source-triage`，不自动事实核验，不自动写回。

## 9. 测试与评测

### 9.1 结构测试

必须覆盖：

- 合法 `low`、`medium`、`high`、`indeterminate`；
- 缺少正文时只能返回 `indeterminate`；
- 四个信号字段齐全；
- 每个信号包含 rating、evidence、confidence；
- 禁止 `ai_generated=true`、`truth_score`、`automatic_action`、`telemetry` 等越界字段；
- `writeback_status` 必须为 `none`。

### 9.2 行为评测集

第一批建议建立 24 个人工标注样本：

| 类型 | 数量 | 目的 |
|---|---:|---|
| `should_trigger` | 8 | 批量模板、无具体来源、只有情绪刺激的内容 |
| `should_not_trigger` | 8 | 有具体来源、案例、作者判断或真实用途的内容 |
| `edge_case` | 4 | 文学、讽刺、广告、娱乐、匿名表达 |
| `neighbor_confusion` | 4 | 只问“是否值得读”的 Source Triage 输入 |

该评测集首先验证边界与解释质量，不宣称模型准确率。后续如需量化，必须由 Founder 或人工评审确认标签标准。

### 9.3 必测反例

1. AI 辅助但有具体来源和作者判断的深度文章，不应因 AI 参与而判高风险。
2. 没有外部来源的个人经历，不应因来源弱而判高风险。
3. 有强情绪但具有真实调查和具体事实的内容，不应仅因情绪强而判高风险。
4. 用户只问“值得不值得读”，不应启动本 Skill。
5. 只有标题和封面，不应输出强风险结论。

## 10. 文件结构

独立 Skill 仓库建议结构：

```text
content-signal-screen/
├── SKILL.md
├── README.md
├── LICENSE
├── LICENSE-STATUS.md
├── FEEDBACK.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── signal-rules.md
│   └── output-templates.md
├── scripts/
│   └── validate_content_signal_screen.py
├── tests/
│   └── test_validate_content_signal_screen.py
└── evals/
    └── content-signal-screen-evals.json
```

不在公开仓库中放入：

- 用户私有原文；
- 未授权文章全文；
- 自动上传脚本；
- 真实用户数据；
- “准确率已证明”之类没有评测依据的宣传材料。

## 11. README 产品叙事要求

README 可以使用以下产品叙事：

> 不是所有 AI 内容都是 slop。真正需要警惕的是：低投入、低信息量、批量生产、只为占用注意力的内容。

> Content Signal Screen 不替你判断真伪，只帮你在继续阅读、转发或发布之前，快速看见内容质量风险。

必须同时写明：

- 它不是 AI 文本检测器；
- 它不是事实核验器；
- 它不是内容审查器；
- 它不会替用户决定是否阅读；
- 它没有遥测、自动上传或自动写回。

## 12. 发布与 GitHub 同步门

### 12.1 本地实现完成条件

- `SKILL.md` 与输出 schema 一致；
- validator 能拒绝缺字段、越界字段和不确定性缺失；
- 单元测试通过；
- 24 个行为评测样本已建立；
- README、示例、许可证和隐私边界完整；
- 公开卫生扫描通过；
- 与 `source-triage` 的邻居混淆测试通过。

### 12.2 GitHub 发布顺序

1. 在本地独立仓库完成实现和测试；
2. 检查工作区只包含本任务文件；
3. 提交有意图的 commit；
4. 创建公开 GitHub 仓库 `content-signal-screen`；
5. 发布 `main` 分支；
6. 通过 GitHub API/raw 内容核对 README、`SKILL.md` 和许可证；
7. 在 `source-triage` README 增加已验收的邻接能力链接；
8. 写发布回执，明确实现、验收、远程内容和未证明事项。

### 12.3 不得声称

- “已准确识别所有 slop”；
- “能识别 AI 生成内容”；
- “能自动过滤互联网垃圾”；
- “已证明节省了多少阅读时间”；
- “文章引用的研究已经被本 Skill 验证”。

## 13. 责任与状态字段

每次实现或发布回执必须分别记录：

```text
implemented:
validated:
published:
remote_content_verified:
effect_proven:
durable_writeback:
not_done:
```

预期的首个工程状态应为：

```text
implemented: false
validated: false
published: false
remote_content_verified: false
effect_proven: false
durable_writeback: false
```

## 14. 实施门

本文件完成后，下一步才可以进入实现阶段。实现阶段应以本文件为约束，不得在实现过程中擅自：

- 把能力并入 `source-triage` 核心输出；
- 添加 AI 检测或事实判断；
- 删除 `indeterminate`；
- 删除邻居混淆测试；
- 把示例结果宣传成效果证明；
- 在 GitHub 远程仓库中发布未通过本地卫生检查的内容。

### 当前完成状态

```text
engineering_spec_written: true
implementation_started: false
source_triage_modified: false
new_skill_created: false
github_updated: false
```
