import logging
import sys
from datetime import date, datetime
from typing import Optional, Union

from mkdocs.config import config_options as opt
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils import DuplicateFilter
from mkdocs.utils.templates import TemplateContext
from pydantic import BaseModel, field_validator

DEFAULT_COLORS = {
    "draft": "#a3a3a3",
    "proposed": "#b6d8ff",
    "accepted": "#b4eda0",
    "rejected": "#ffd5d1",
    "superseded": "#ffebb6",
}


class AdrPluginConfig(Config):
    graph_file = opt.Optional(opt.Type(str))
    mermaid_color = opt.Type(dict, default=DEFAULT_COLORS)


class Record(BaseModel):
    title: str
    id: str
    url: str
    tags: list[str] = []
    status: str
    author: str
    created: date
    superseded_by: Optional[Union[str, "Record"]] = None
    extends: list[Union[str, "Record"]] = []
    base: list[Union[str, "Record"]] = []

    @field_validator("created", mode="before")
    def parse_created(cls, value):
        return datetime.strptime(value, "%d-%b-%Y").date()

    @classmethod
    def build_from_page(cls, page: Page) -> "Record":
        return cls(
            title=page.title,
            id=_get_id_from_page(page),
            url=page.abs_url if page.abs_url else page.url,
            tags=page.meta.get("tags", []),
            **page.meta.get("adr"),
        )


class RecordCollection:
    def __init__(self) -> None:
        self._root = []
        self._map: dict[str, Record] = {}

    def add(self, record: Record) -> None:
        self._map[record.id] = record

    def get(self, id: str) -> Optional[Record]:
        self._build()
        return self._map.get(id)

    def _build(self) -> None:
        for _, record in self._map.items():
            _super = record.superseded_by
            if _super and isinstance(_super, str):
                record.superseded_by = self._map[_super]

            ext = []
            for r_ext in record.extends:
                if isinstance(r_ext, str):
                    r_ext = self._map[r_ext]

                if record not in r_ext.base:
                    r_ext.base.append(record)

                ext.append(r_ext)
            record.extends = ext

    def generate_graph(self, colors: dict[str, str]) -> str:
        self._build()
        graph = ["```mermaid", "graph TD"]
        for r in self._map.values():
            graph.append(f"{r.id}[{r.title}]")
            graph.append(f'click {r.id} "{r.url}" _blank')
            graph.append(f"{r.id}:::mermaid-{r.status}")
            graph.append(f"{r.id}:::mermaid-common")

            if r.superseded_by:
                graph.append(f"{r.id} -- Superseded --> {r.superseded_by.id}")
            for r2 in r.extends:
                graph.append(f"{r2.id} -- Extended --> {r.id}")

        for key, color in colors.items():
            graph.append(f"classDef mermaid-{key} fill:{color};")
            graph.append("classDef mermaid-common color:#595959;")

        graph.append("```")
        return "\n".join(graph)


# adr plugin
class AdrPlugin(BasePlugin[AdrPluginConfig]):
    # init plugin
    def on_config(self, config: MkDocsConfig) -> Optional[MkDocsConfig]:
        self.graph_file = None
        self.record_collection = RecordCollection()

    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files
    ) -> Optional[Navigation]:
        # append file at the end for one last pass
        path = self.config.graph_file
        if path:
            self.graph_file = files.get_file_from_path(path)
            if not self.graph_file:
                log.error(f"Graph file '{path}' does not exist.")
                sys.exit(1)
            files.remove(self.graph_file)
            files.append(self.graph_file)

    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> Optional[str]:
        if page.file == self.graph_file:
            return markdown.replace(
                "[GRAPH]",
                self.record_collection.generate_graph(self.config.mermaid_color),
            )

        if page.meta.get("adr") is None:
            return

        self.record_collection.add(Record.build_from_page(page))

    def on_page_context(
        self,
        context: TemplateContext,
        *,
        page: Page,
        config: MkDocsConfig,
        nav: Navigation,
    ) -> Optional[TemplateContext]:
        if page.meta.get("adr") is None:
            return

        record = self.record_collection.get(_get_id_from_page(page))
        context["adr"] = record
        return context


def _get_id_from_page(page: Page) -> str:
    return page.url.split("/")[-2]


log = logging.getLogger("mkdocs")
log.addFilter(DuplicateFilter())
