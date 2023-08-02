# ADR for MkDocs's Material Theme

[ADR](https://lyz-code.github.io/blue-book/adr/) are short text documents that captures an important architectural decision made along with its context and consequences.

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
WIP
