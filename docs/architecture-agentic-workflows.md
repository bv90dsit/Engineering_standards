# Agentic Workflows — Architecture

Potential AI-powered automation for this repo. Each workflow is independent — they can be adopted incrementally.

## Overview

```mermaid
graph TB
    subgraph Triggers
        ISSUE[GitHub Issue<br/>label: new-standard]
        CRON[Weekly schedule]
        PR[Pull Request<br/>touches modules/**]
        MCP_REQ[MCP request<br/>from external team]
        MANUAL[Manual trigger]
    end

    subgraph Agents
        A1[Standard Authoring<br/>Agent]
        A2[Source Monitoring<br/>Agent]
        A3[PR Review<br/>Agent]
        A4[Compliance Report<br/>Agent]
        A5[Research<br/>Agent]
    end

    subgraph Actions
        SCAFFOLD[Scaffold standard]
        VALIDATE[Run validation]
        BUILD_GRAPH[Rebuild graph]
        BUILD_SKILL[Rebuild skill]
        OPEN_PR[Open PR]
        POST_COMMENT[Post review comment]
        OPEN_ISSUE[Open issue]
        GENERATE_REPORT[Generate report]
    end

    subgraph External
        CLAUDE[Claude API]
        GH[GitHub API]
        SOURCES[Source URLs<br/>NCSC, OWASP, GDS...]
    end

    ISSUE --> A1
    CRON --> A2
    PR --> A3
    MCP_REQ --> A4
    MANUAL --> A5

    A1 --> CLAUDE
    A1 --> SCAFFOLD
    A1 --> VALIDATE
    A1 --> BUILD_GRAPH
    A1 --> BUILD_SKILL
    A1 --> OPEN_PR

    A2 --> SOURCES
    A2 --> OPEN_ISSUE

    A3 --> VALIDATE
    A3 --> POST_COMMENT

    A4 --> GENERATE_REPORT

    A5 --> CLAUDE
    A5 --> OPEN_ISSUE

    OPEN_PR --> GH
    POST_COMMENT --> GH
    OPEN_ISSUE --> GH
```

## Workflow Details

### 1. Standard Authoring Agent (highest value)

```mermaid
sequenceDiagram
    participant User
    participant GitHub
    participant Agent
    participant Claude
    participant Repo

    User->>GitHub: Opens issue (free-text or template)
    GitHub->>Agent: Webhook trigger (label: new-standard)
    Agent->>Claude: Interpret issue — extract intent, category, sources
    Claude-->>Agent: Structured output (ID, module, conformance, sources, rationale)
    Agent->>Repo: Scaffold standard file (modules/*/standards/*.md)
    Agent->>Repo: Update index.yaml
    Agent->>Repo: Rebuild graph data
    Agent->>Repo: Rebuild skill
    Agent->>Repo: Run validate_standards.py
    Agent->>GitHub: Open PR with all changes
    GitHub-->>User: PR ready for review
```

**Requires:** `ANTHROPIC_API_KEY` repo secret

**Eliminates:** Manual multi-file creation, graph drift, forgotten index updates

---

### 2. Source Monitoring Agent

```mermaid
sequenceDiagram
    participant Cron
    participant Agent
    participant Sources
    participant GitHub

    Cron->>Agent: Weekly trigger
    loop For each source URL in trusted_sources.yaml
        Agent->>Sources: HEAD request (check last-modified / status)
    end
    Agent->>Agent: Compare against last-known state
    alt Source has changed
        Agent->>GitHub: Open issue — "NCSC updated Secure by Design guidance"
        Note over GitHub: Lists affected standards (from graph data)
    end
```

**Requires:** No API key (just HTTP requests + GitHub token)

**Eliminates:** Stale standards based on outdated source material

---

### 3. PR Review Agent

```mermaid
sequenceDiagram
    participant Dev
    participant GitHub
    participant Agent
    participant Repo

    Dev->>GitHub: Opens PR touching modules/**
    GitHub->>Agent: PR event trigger
    Agent->>Repo: Run validate_standards.py
    Agent->>Repo: Run check_graph_sync.py
    Agent->>Repo: Run impact_analysis.py
    Agent->>Agent: Check source URLs are reachable
    Agent->>GitHub: Post structured review comment
    Note over GitHub: Validation ✓/✗, Impact summary, URL status
```

**Requires:** No API key (script-based checks + GitHub token)

**Eliminates:** Missed validation in review, manual impact assessment

---

### 4. Compliance Report Agent

```mermaid
sequenceDiagram
    participant Team
    participant MCP
    participant Agent
    participant TeamRepo

    Team->>MCP: "Check our repo against python standards"
    MCP->>Agent: Trigger with repo URL + filters
    Agent->>TeamRepo: Clone / read
    Agent->>Agent: Run check_compliance.py
    Agent->>MCP: Return structured report (PASS/FAIL per standard)
    MCP-->>Team: Formatted compliance report
```

**Requires:** MCP server running, access to target repo

**Eliminates:** Manual compliance checks, teams guessing which standards apply

---

### 5. Cross-Government Research Agent

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Claude
    participant Web
    participant GitHub

    User->>Agent: Manual trigger or schedule
    Agent->>Web: Search GDS blog, NCSC updates, CDDO announcements
    Agent->>Claude: Summarise findings — what's new, what affects us
    Claude-->>Agent: Summary + recommendations
    alt New guidance found
        Agent->>GitHub: Open issue with summary + proposed new standards
    else No changes
        Agent->>Agent: Log "no updates" — silent
    end
```

**Requires:** `ANTHROPIC_API_KEY`, web access

**Eliminates:** Missing new government guidance, reactive rather than proactive updates

---

## Dependencies

| Workflow | GitHub Token | Anthropic API Key | Web Access | MCP Server |
|----------|:---:|:---:|:---:|:---:|
| 1. Standard Authoring | Yes | Yes | No | No |
| 2. Source Monitoring | Yes | No | Yes | No |
| 3. PR Review | Yes | No | No | No |
| 4. Compliance Report | No | No | No | Yes |
| 5. Research | Yes | Yes | Yes | No |

## Recommended adoption order

1. **PR Review Agent** — lowest barrier (no API key), immediate value, catches what CI misses
2. **Standard Authoring Agent** — highest value, needs API key
3. **Source Monitoring Agent** — fire-and-forget, catches staleness
4. **Compliance Report Agent** — serves other teams, depends on MCP adoption
5. **Research Agent** — nice-to-have, highest complexity
