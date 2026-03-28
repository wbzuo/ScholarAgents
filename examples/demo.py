from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scholaragents.artifacts.artifact_store import ArtifactStore
from scholaragents.core.orchestrator import MultiAgentSystem


def main() -> None:
    system = MultiAgentSystem()
    artifact_store = ArtifactStore(root_dir=PROJECT_ROOT / "outputs")
    queries = [
        "帮我整理干旱监测方向的文献",
        "帮我写 methods 章节",
        "帮我设计 SPEI 预测实验和消融实验",
        "我想做一个课题组多agent平台",
        "请帮我完成干旱监测方向的文献综述",
        "请结合 related work 帮我写 drought monitoring 论文 introduction",
        "请帮我设计 SPEI 预测实验，并写 experiments 章节框架",
    ]

    for index, query in enumerate(queries, start=1):
        response = system.handle(user_id="demo_user", query=query)

        print(f"Case {index}")
        print(f"用户问题: {query}")
        print(f"是否触发 workflow: {response['workflow_triggered']}")
        if response["workflow_triggered"]:
            print(f"Workflow 名称: {response['workflow_name']}")
        else:
            print(f"选择的 Agent: {response['selected_agent']}")
        print("最终结果:")
        print(response["result"])
        shared_memory = response["shared_memory"]
        artifact = response.get("artifact")
        if artifact:
            print("Artifact 摘要:")
            print(f"- title: {artifact.get('title')}")
            print(
                f"- sections: {[section.get('name') for section in artifact.get('sections', [])]}"
            )
            print(f"- next_actions: {artifact.get('next_actions')}")
            if response["workflow_triggered"]:
                case_name = f"case_{index}"
                task_info = shared_memory.get("task_info", {}) if response["shared_memory"] else {}
                task_plan = shared_memory.get("task_plan", []) if response["shared_memory"] else []
                export_paths = artifact_store.save_artifact(
                    artifact=artifact,
                    case_name=case_name,
                    workflow_name=response["workflow_name"],
                    query=query,
                    selected_writing_mode=task_info.get("selected_writing_mode"),
                    task_plan=task_plan,
                )
                print("导出文件:")
                print(f"- markdown: {export_paths['markdown']}")
                print(f"- json: {export_paths['json']}")
                print(f"- index: {export_paths['index']}")
        print("Trace:")
        for trace in response["traces"]:
            print(f"- {trace}")
        print("Shared Memory:")
        if shared_memory:
            print(f"- task_info: {shared_memory.get('task_info')}")
            print(f"- task_plan: {shared_memory.get('task_plan')}")
            print(f"- intermediate_results: {shared_memory.get('intermediate_results')}")
            print(f"- skill_records: {shared_memory.get('skill_records')}")
            print(f"- final_result: {shared_memory.get('final_result')}")
        else:
            print("- {}")
        print("-" * 60)


if __name__ == "__main__":
    main()
