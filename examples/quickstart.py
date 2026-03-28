from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scholaragents.core.orchestrator import MultiAgentSystem


if __name__ == "__main__":
    system = MultiAgentSystem()
    result = system.handle(user_id="quickstart_user", query="帮我整理干旱监测方向的文献调研")
    print(result)
