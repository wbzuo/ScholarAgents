from __future__ import annotations

from typing import Iterable

from .base_skill import BaseSkill


class ResultFormattingSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("result_formatting")

    def execute(
        self,
        title: str,
        sections: Iterable[str],
        intro: str | None = None,
    ) -> dict:
        section_list = list(sections)
        lines = [title]
        if intro:
            lines.append(intro)

        for index, section in enumerate(section_list, start=1):
            formatted_section = str(section).replace("\n", "\n   ")
            lines.append(f"{index}. {formatted_section}")

        content = "\n".join(lines)
        return self.build_output(
            content=content,
            title=title,
            section_count=len(section_list),
            has_intro=intro is not None,
        )
