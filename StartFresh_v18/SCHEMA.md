# Wiki OS Data Schemas

To ensure deterministic parsing and consistent behavior, all generated assets must conform to the following schemas.

## 1. Markdown (.md) Entity Pages
Saved in `wiki/entities/`. Every synthesized entity, concept, or summary page must include YAML frontmatter and consistent linkage.

```yaml
---
id: string (unique UUID or slug)
type: enum (entity | concept | summary | synthesis)
tags: list(string)
inbound_links: int (updated by maintenance skill)
confidence: float (0.0 to 1.0)
last_ingested_sources: list(string)
---
```

**Body Requirements:**
- Must contain an `# Overview`.
- Must contain a `## Citations` section where all facts have explicit relative links to the `raw/` files.
- Must contain a `## Related Nodes` section holding bidirectional links to other `.md` pages in the wiki.

## 2. XML (.xml) Tabular Data
For strictly structured grids mapping 1:1 data relations that cannot easily be parsed by standard markdown tables without breaking syntax, we strictly enforce `.xml`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DataGrid id="grid_xyz123" origin_source="raw/finances_2026.pdf">
    <Columns>
        <Column type="string" name="EntityName" />
        <Column type="number" name="Value" />
        <Column type="string" name="Notes" />
    </Columns>
    <Rows>
        <Row>
            <EntityName>Acme Corp</EntityName>
            <Value>10000</Value>
            <Notes>Initial investment</Notes>
        </Row>
    </Rows>
</DataGrid>
```
*Note: Any XML viewer or Obsidian plugins (such as Dataview or specific XML-to-Markdown renderer plugins) can easily load this document via standard XPath targeting the `<Row>` elements.*

## 3. JSON (.json) Memory 
Maintains continuous episodic conversational memory for agents.

```json
{
  "session_id": "sess_89b2",
  "agent_id": "claude_v3_analyst",
  "timestamp": "2026-04-21T09:00:00Z",
  "context_loaded": ["wiki/concepts/AI_OS.md"],
  "exchanges": [
    {
      "role": "human",
      "content": "Analyze these two sources for contradictions."
    },
    {
      "role": "agent",
      "content": "Based on my semantic graph traversal..."
    }
  ],
  "action_taken": "UPDATED_GRAPH"
}
```

## 4. JSON (.json) Inter-Agent Job Protocol
Used to pass multi-step workflows between agents without human intervention. Stored in `/jobs/pending/`.

```json
{
  "job_id": "job_audio_ingest_77a",
  "status": "pending",
  "priority": "high",
  "source_uri": "raw/meeting_april_20.mp3",
  "workflow": [
    {
      "step": 1,
      "assigned_agent": "skill_cloud_audio_transcriber",
      "action": "transcribe_audio_to_raw_text"
    },
    {
      "step": 2,
      "assigned_agent": "skill_summarizer",
      "action": "synthesize_md",
      "dependencies": ["step_1"]
    },
    {
      "step": 3,
      "assigned_agent": "skill_graph_weaver",
      "action": "update_inbound_links",
      "dependencies": ["step_2"]
    }
  ]
}
```
