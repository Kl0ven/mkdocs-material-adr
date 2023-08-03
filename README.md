# ADR for MkDocs's Material Theme

[ADR](https://lyz-code.github.io/blue-book/adr/) are short text documents that captures an important architectural decision made along with its context and consequences.


[Demo](http://blog.kloven.fr/mkdocs-material-adr/)

## Install

```bash
pip install mkdocs-material-adr
# or
poetry add mkdocs-material-adr
```

In the `mkdocs.yml` file

```yaml
theme:
  # set the name
  name: mkdocs-material-adr

  # Configuration for the material theme
  features:
    - navigation.instant


plugins:
  - mkdocs-material-adr/adr
```

## Features

### ADR Headers
Information about the ADR are displayed in a header
Define information about the ADR in the frontmatter.

![Alt text](https://raw.githubusercontent.com/Kl0ven/mkdocs-material-adr/main/docs/assets/header.png)


```md
---
    title: 0004 Title
    adr:
        author: Jean-Loup Monnier
        created: 01-Aug-2023
        status:  draft | proposed | rejected | accepted | superseded
        superseded_by: 0001-test
        extends:
            - 0001-first
            - 0002-second
---
```
You can change the colors or add new status using css

```css
/* Background color */
.c-pill-<lower_case_status_name> {
    background: #a3a3a3;
}

/* Dot color */
.c-pill-<lower_case_status_name>:before {
    background: #505050;
}
```

### ADR Graph
Auto generated graph.
To enable it add `[GRAPH]` in the markdown file you want the graph to be, Then add th following configuration

```yaml


plugins:
  - mkdocs-material-adr/adr:
      graph_file: index.md # Change this to your file

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
      - name: mermaid
        class: mermaid
        format: !!python/name:pymdownx.superfences.fence_code_format
```
![Alt text](https://raw.githubusercontent.com/Kl0ven/mkdocs-material-adr/main/docs/assets/graph.png)
