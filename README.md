# Source Triage

> **不要把每一个链接，都变成一个研究项目。**
>
> Source Triage 在你投入阅读之前，先帮你决定：跳过、稍后读、仅作参考、花 5-15 分钟快速筛读，还是值得进入深读。

文章、PDF、报告、书籍、访谈和网页真正昂贵的地方，不是打开它们，而是它们会悄悄占用你的注意力。

多数来源并不需要立刻全文总结，更不需要自动进入研究流程。它们首先需要的是一个判断：**这份材料现在值得占用多少注意力？**

## 当前能做什么

Source Triage 只返回一个有边界的阅读建议：

| 决策 | 含义 |
|---|---|
| `quick_read_now` | 现在花 5-15 分钟进行有限筛读。 |
| `read_deep_now` | 当前决策足以证明值得投入 30-60+ 分钟深读或研究。 |
| `project_relevant_but_not_now` | 与已说明的项目有关，但当前时机不对。 |
| `reference_only` | 保留为参考索引，现在不深读。 |
| `defer_or_monitor` | 未来可能有用，在明确触发条件出现时再回看。 |
| `do_not_invest_further_now` | 可逆地决定：现在不继续投入注意力。 |
| `pending_context` | 来源或当前决策信息不足，暂不能负责地判断。 |

输出会说明：为什么、实际看了哪些部分、不确定什么、刻意没有推断什么，以及建议的下一道关口。

```text
这份来源现在值得读吗？
          |
          v
跳过 / 延后 / 仅作参考 / 快速筛读 / 进入深读
```

## 为什么它故意很小

这不是把全文总结伪装成一个 Skill，而是一个**停止门**。

它不会：

- 认证事实或判断真伪；
- 全文总结或替代深度研究；
- 自动路由项目、创建任务或写入长期记忆；
- 自动安装其他 Skill；
- 在给出建议后自动执行下一步；
- 把示例、反馈或模型偏好说成因果效果证明。

如果 10 分钟筛读已经足够，就不应该把它膨胀成 90 分钟工作流。

## 示例

```text
triage_decision: quick_read_now
basis: 这份报告范围很广，但摘要和一个分类章节足以判断是否需要继续研究。
input_coverage: abstract_and_toc
inspected_sections: [摘要, 目录]
fit_target: 当前工具选型决策
confidence: medium
uncertainty: 尚未核验详细证据与来源质量。
recommended_next_gate: 花 10-15 分钟阅读摘要、结论和最相关的一个章节；再决定是否明确请求深度分析。
writeback_status: none
```

## 一个刻意保留的未来方向

Source Triage 是一个最小但完整的入口：**先决定注意力，再由用户决定是否继续。**

未来可以在用户明确请求后，衔接到更深的来源学习流程，例如：带来源定位的阅读笔记、方法蒸馏和可复用学习候选。

```text
当前 Skill：决定注意力
未来可选流程：用户明确要求后，再从来源中学习
```

这只是方向，不是当前已实现功能，更不是自动研究、自动行动或自动写入任何系统的承诺。即使以后不接任何后续流程，今天这个“先决定要不要读”的入口也应当独立有用。

## 快速使用与接入

这个仓库下载下来就是一个标准的 Skill 包：核心是 `SKILL.md`，并包含示例、校验脚本和参考规则。不同工具的接入方式不同。

### Codex

Codex 可以直接使用这个包。将仓库克隆到你的 Codex Skill 目录：

**Windows PowerShell：**

```powershell
git clone https://github.com/007M7/source-triage.git "$HOME\.codex\skills\source-triage"
```

**macOS / Linux：**

```bash
git clone https://github.com/007M7/source-triage.git ~/.codex/skills/source-triage
```

重新打开 Codex 或新建一个任务后，直接说：

```text
请用 source-triage 判断这份 PDF 是否值得我现在读。
```

也可以更明确地写：

```text
请使用 $source-triage：这是链接/文件路径；我的当前目标是…??
```

如果你的 Codex 工作区提供 Skills 页面或上传入口，也可以将这个仓库下载后的文件夹作为 Skill 导入。`SKILL.md` 是这个包的核心说明文件。

### Claude Code

**???????** Claude Code ? Skills ?? Agent Skills ???????????????? `SKILL.md`?????????????????

**???????? Claude Code ????**

```bash
git clone https://github.com/007M7/source-triage.git ~/.claude/skills/source-triage
```

**??????????????**

```bash
mkdir -p .claude/skills
git clone https://github.com/007M7/source-triage.git .claude/skills/source-triage
```

?? Claude Code ?????????

```text
/source-triage
```

????????????????

```text
???????????????????????????????
```

Claude Code ??? `SKILL.md` ????????????? `source-triage` ?? `/source-triage` ??????????? `CLAUDE.md` ????

### 最短使用提示

无论使用 Codex 还是 Claude Code，给出以下三类信息会让判断更可靠：

```text
1. 来源：链接、文件路径、标题、摘要或目录。
2. 你的当前目标：例如选型、研究、写作、项目决策或个人阅读队列。
3. 注意力约束：现在只想花 10 分钟，还是愿意投入一小时深读。
```

## 隐私与反馈

查看 `FEEDBACK.md`。反馈完全自愿，默认本地处理；没有遥测、没有自动上传来源、没有自动保存，也不会自动被当成效果证明。

## 本地验证

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_source_triage.py examples/quick-read-now.source-triage.json
```

## 开源状态

本项目使用 MIT License。你可以使用、修改和分发本项目，但请保留许可证和版权声明；软件按“现状”提供，不附带保证。