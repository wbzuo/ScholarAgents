# ScholarAgents v0.9 发布说明 / CHANGELOG

## 版本信息

版本号：`v0.9`  
版本定位：多 Agent 原型系统进入“可运行 + 可解释 + 可导出 + 可接模型层”的阶段。

## 一、版本概述

ScholarAgents v0.9 在前期多 Agent 原型的基础上，完成了从“单一规则路由 demo”到“多 workflow、结构化 artifact、可导出成果物、支持模型层扩展”的系统演进。

本版本重点不再只是让系统“能回答”，而是让系统具备：

- 多 Agent 协作能力
- 多 workflow 分流能力
- 轻量 planner 能力
- shared memory 上下文共享能力
- skill 驱动的生成能力
- artifact 结构化输出能力
- Markdown / JSON 导出能力
- 后续接入真实大模型的架构基础

## 二、本版本已实现能力

### 1. 单 Agent 路由

系统支持根据用户 query 自动路由到对应 Agent，包括但不限于：

- `literature_agent`
- `writing_agent`
- `experiment_agent`
- `general_agent`

对于普通请求，系统保持单 Agent 响应模式不变。

### 2. 多 workflow 分流

本版本已支持至少 3 个 workflow。

#### `literature_review_workflow`

适用于：

- 文献整理
- 文献综述
- related work
- 研究现状分析

执行链路：

- `LiteratureAgent -> WritingAgent -> GeneralAgent`

#### `paper_writing_workflow`

适用于：

- introduction
- related work 驱动的论文写作
- 写作与文献支撑结合场景

执行链路：

- `LiteratureAgent -> WritingAgent -> GeneralAgent`

#### `experiment_design_workflow`

适用于：

- 实验设计
- experiments 章节框架
- baseline / 指标 / 消融设计

执行链路：

- `ExperimentAgent -> WritingAgent -> GeneralAgent`

系统已支持 workflow 候选检测、优先级选择和选择理由解释。

### 3. Planner / Task Plan

本版本增加了轻量规划能力。

在 workflow 执行前，系统会先生成任务计划，并写入：

- trace
- shared memory

例如：

- `plan step 1: LiteratureAgent -> 整理文献`
- `plan step 2: WritingAgent -> 生成综述骨架`
- `plan step 3: GeneralAgent -> 给出扩写建议`

这使系统具备“先规划、后执行”的可解释能力。

### 4. Shared Memory

本版本 workflow 已支持共享上下文与中间结果。

当前 shared memory 中至少包括：

- `task_info`
- `task_plan`
- `intermediate_results`
- `skill_records`
- `final_result`

其中 `task_info` 已支持记录：

- `workflow_name`
- `selected_workflow`
- `selected_writing_mode`
- `model_provider`
- `model_name`

shared memory 使得多个 Agent 可以在同一任务链中传递上下文，而不再只是简单拼接字符串。

### 5. Skill 层接入

本版本已将核心生成能力抽离为 skill，形成：

- `PaperSearchSkill`
- `PaperSummarySkill`
- `OutlineGenerationSkill`
- `ExperimentPlanningSkill`
- `ResultFormattingSkill`

当前 trace 已能明确显示 skill 调用链，例如：

- `LiteratureAgent calling PaperSummarySkill`
- `WritingAgent calling OutlineGenerationSkill with mode=...`
- `ExperimentAgent calling ExperimentPlanningSkill`
- `... calling ResultFormattingSkill`

这意味着系统已从“Agent 内部硬编码模板”升级为“Agent 调 Skill”的结构。

### 6. 写作模式（mode-aware generation）

`WritingAgent` 已支持按任务场景选择不同 mode。

当前已看到的模式包括：

- `literature_review`
- `method_section`
- `introduction_related_work`
- `experiment_section`

这使系统能够根据不同任务生成更贴近学术写作场景的结构，而不是复用同一套泛化模板。

### 7. Workflow Summary Mode

`GeneralAgent` 在 workflow 场景中不再只是简单兜底，而是开始承担总结与下一步建议的角色。

例如：

- literature workflow -> related work 初稿建议
- paper writing workflow -> introduction 扩写建议
- experiment workflow -> experiments 章节组织建议

这使得 workflow 输出更完整，也更接近真实科研辅助流程。

### 8. Structured Artifact Output

本版本新增统一的 artifact 输出对象。

artifact 当前至少包含：

- `title`
- `sections`
- `next_actions`
- `raw_text`

例如 demo 中已出现：

- `Literature Review Artifact`
- `Paper Writing Artifact`
- `Experiment Design Artifact`

单 Agent 与 workflow 都已兼容 artifact 输出。

### 9. Artifact Export & Persistence

本版本已支持将 artifact 持久化导出到本地文件系统。

当前支持：

- Markdown 导出
- JSON 导出
- artifact 索引文件维护

输出目录包括：

- `outputs/markdown/`
- `outputs/json/`
- `outputs/artifact_index.json`

demo 输出中已经能打印具体导出路径。

### 10. Trace / Explainability

系统已具备较完整的 trace 输出机制，当前可记录：

- 收到 query
- workflow 候选
- workflow 选择理由
- task plan
- agent 执行步骤
- skill 调用链
- result formatting
- workflow 完成

这使 ScholarAgents 具备较好的可解释性，也为后续调试、评估和前端展示提供了基础。

### 11. Models Layer

本版本已接入统一模型层，支持：

- `mock` provider
- `openai` provider
- `BaseModelClient`
- `model_factory`
- `generation_config`
- `response_parser`
- `retry_policy`
- `usage_tracker`
- 失败 fallback 到 mock 的基础能力

当前核心 skills 已通过统一的 `model_client` 调用生成能力，trace 中可记录 provider，workflow shared memory 中也可追溯 `model_provider` 与 `model_name`。

### 12. v0.10 起步：检索增强

在当前版本基础上，仓库已经开始进入 v0.10 的第一步演进：

- 将 `PaperSearchSkill` 接入文献主链路
- 将 `ArxivMCPClient` 作为本地可运行的检索 stub 接入
- 在文献相关流程中先检索候选论文，再生成综述型结果
- 将检索结果写入 trace、skill metadata 与 shared memory

这让系统开始从“纯模板化文献整理”走向“检索增强的文献工作流”。

## 三、目录结构（当前核心模块）

```text
ScholarAgents/
├── scholaragents/
│   ├── core/
│   ├── agents/
│   ├── workflows/
│   ├── skills/
│   ├── memory/
│   ├── artifacts/
│   ├── models/          # 已接入的统一模型层（mock / openai）
│   └── utils/
├── examples/
├── outputs/
│   ├── markdown/
│   ├── json/
│   └── artifact_index.json
├── tests/
├── README.md
└── pyproject.toml
```

## 四、运行方式

### 默认运行

```bash
python examples/demo.py
```

### mock 模式

```bash
MODEL_PROVIDER=mock python examples/demo.py
```

### openai 模式

```bash
MODEL_PROVIDER=openai OPENAI_API_KEY=YOUR_KEY OPENAI_MODEL=gpt-5.4 python examples/demo.py
```

真实模型模式已预留完整接入路径；在安装 OpenAI SDK 并配置 `OPENAI_API_KEY` 后，可看到 provider / model trace。若未配置 key 或 SDK，系统会按配置 fallback 到 mock。

## 五、建议补跑的验收命令

```bash
python -m compileall scholaragents examples
python examples/demo.py
MODEL_PROVIDER=mock python examples/demo.py
MODEL_PROVIDER=openai OPENAI_API_KEY=xxx OPENAI_MODEL=gpt-5.4 python examples/demo.py
```

## 六、v0.9 验收结果模板

下面这段可以直接放进 release note 末尾作为验收记录。

### 模型层与基础能力

- [x] mock 模式可正常运行
- [ ] openai 模式可正常运行
- [x] 无 API key 时可 fallback 或给出清晰错误
- [x] trace 中可记录 provider / model

### Skill 与 Workflow

- [x] `PaperSummarySkill` 已接入主链路
- [x] `OutlineGenerationSkill` 已接入主链路
- [x] `ExperimentPlanningSkill` 已接入主链路
- [x] 3 个 workflow 正常运行
- [x] 单 Agent 路由保持兼容

### Shared Memory 与 Artifact

- [x] `task_info` 正常写入
- [x] `task_plan` 正常写入
- [x] `intermediate_results` 正常写入
- [x] `skill_records` 正常写入
- [x] `final_result` 正常写入
- [x] artifact 正常生成
- [x] Markdown / JSON 导出正常
- [x] `artifact_index.json` 正常更新

## 七、已知限制

当前版本仍存在以下限制。

1. workflow 路由主要基于规则关键词
   还不是模型驱动的任务分解器。

2. provider 仍处于扩展阶段
   当前目标 provider 为 `mock / openai`，暂未体现更多 provider。

3. 外部平台集成尚未正式接入
   飞书 / Notion / GitHub / 文件系统集成仍以占位或后续版本为主。

4. 文献检索仍偏模板化
   当前 `PaperSummarySkill` 等更像结构化生成原型，真实 paper search / citation retrieval 还未 fully integrated。

5. artifact index 仍是基础版本
   还没有浏览页、检索页或前端界面。

## 八、下一步开发方向

### v0.10 推荐方向：Models Layer 深化

重点：

- 更稳定的 `mock / openai` 双 provider
- 更完善的 `usage_tracker`
- 更细的 `response_parser`
- 更明确的模型调用审计
- 更丰富的 fallback 与错误恢复策略

### 后续方向

- 更强的 model routing
- skill registry
- integration / MCP
- artifact index 浏览页
- 外部平台（飞书 / Notion）对接
- 真实 paper search / retrieval 接入

## 九、一句话总结

ScholarAgents v0.9 已经从“多 Agent 架构原型”演进为“具备多 workflow、共享记忆、结构化 artifact、成果物导出、统一模型层和可解释执行链路的科研协同系统原型”。
