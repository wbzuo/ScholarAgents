from __future__ import annotations


class WorkflowPlanner:
    """Lightweight rule-based planner for workflow execution."""

    def generate_plan(self, workflow_name: str) -> list[dict[str, str]]:
        plans: dict[str, list[dict[str, str]]] = {
            "literature_review_workflow": [
                {
                    "step": "1",
                    "agent": "LiteratureAgent",
                    "action": "整理文献",
                },
                {
                    "step": "2",
                    "agent": "WritingAgent",
                    "action": "生成综述骨架",
                },
                {
                    "step": "3",
                    "agent": "GeneralAgent",
                    "action": "给出 related work 扩写建议",
                },
            ],
            "paper_writing_workflow": [
                {
                    "step": "1",
                    "agent": "LiteratureAgent",
                    "action": "提供相关研究支撑",
                },
                {
                    "step": "2",
                    "agent": "WritingAgent",
                    "action": "生成 introduction/related work 骨架",
                },
                {
                    "step": "3",
                    "agent": "GeneralAgent",
                    "action": "给出扩写建议",
                },
            ],
            "experiment_design_workflow": [
                {
                    "step": "1",
                    "agent": "ExperimentAgent",
                    "action": "生成实验设计",
                },
                {
                    "step": "2",
                    "agent": "WritingAgent",
                    "action": "生成 experiments 章节框架",
                },
                {
                    "step": "3",
                    "agent": "GeneralAgent",
                    "action": "给出章节组织建议",
                },
            ],
        }
        return plans.get(workflow_name, [])
