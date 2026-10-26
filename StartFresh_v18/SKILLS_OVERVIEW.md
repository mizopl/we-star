# Wiki OS Skill Definitions

This module describes the core skillset available to the Autonomous Knowledge Base agent. They can be triggered by human prompts, timed cron jobs, or inter-agent job protocols.

## 1. Multimodal Ingestion Pipeline (`skill_ingest_source`)
The entry point for bringing immutable knowledge into the system.

**Inputs:** URI of the raw file (text, audio, image).
**Process:**
1. **Audio/Video Extraction:** If audio/video, triggers a cloud-based transcription tool (like ElevenLabs) to dump an audio-log transcript text file.
2. **Vision Extraction:** If image, uses a Vision model to describe the scene or extract OCR text.
3. **Format Routing:** 
   - Detects if the internal structure is inherently tabular (financial reports, spreadsheets, rigid schedules). If so, maps data to a `.xml` grid using the `<DataGrid>` schema.
   - Otherwise, parses the content into a fundamental `.md` file, extracting key entities.
**Outputs:** Creation of `raw/...` files and the initiation of a `skill_summarize` job.

## 2. Summarization & Indexing (`skill_summarize`)
Responsible for abstracting the raw ingest into the actual Wiki OS.

**Inputs:** Raw text file URI.
**Process:**
1. Reads the raw text, isolating core themes, claims, and entities.
2. Checks the `index.md` to see if `.md` pages for these entities already exist. 
3. Updates `index.md` with new entries or bumps the `last_updated` properties of existing entries.
4. Generates standard Entity `.md` pages complete with YAML frontmatter.
**Outputs:** New or updated `.md` files in the `/wiki` directory.

## 3. Meta-Knowledge Weaver (`skill_graph_weaver`)
The mechanism that gives the Knowledge Base its "Brain" capabilities.

**Inputs:** A newly created/updated wiki `.md` file.
**Process:**
1. Scans existing `.md` files across the `/wiki` directory using high-speed similarity search or regex match for related conceptual keywords.
2. Cross-references the new file with older existing files.
3. Injects bidirectional markdown links `[[Concept Name]]` into both files.
4. Updates the `inbound_links` counter in the YAML frontmatter of the associated files, giving the Graph View weight and gravity.
**Outputs:** Heavily cross-linked `.md` files.

## 4. Q&A and Synthesis (`skill_query_synthesize`)
The primary interface for the Human to converse with the knowledge base.

**Inputs:** A human conversational prompt.
**Process:**
1. The agent searches the `.md` semantic layer (NOT the raw layer unless deep citations are needed).
2. Synthesizes a response to the prompt.
3. **Crucial Step:** If the resulting synthesis generates a *net-new* conceptual realization, it automatically triggers `write_synthesis_to_wiki` to create a permanent new `.md` page.

## 5. "Blue Ocean" Discovery (`skill_blue_ocean_linter`)
An active background process for finding gaps in the knowledge graph.

**Inputs:** The complete `/wiki` directory.
**Process:**
1. Runs a heuristic scan over the YAML metadata looking for orphan nodes (nodes with `inbound_links: 0`).
2. Looks for semantic collisions mapping to the same name or contradictory facts extracted from conflicting sources.
3. Generates a `Blue Ocean Report.md` highlighting what is not known and where contradictions exist.

## 6. Background Researcher & Forecaster (`skill_recurring_research`)
A cron-based, recurring task skill designed to proactively dig deeper without human prompting.

**Inputs:** Empty gaps identified by the `Blue Ocean Linter` or highly trafficked nodes in `index.md`.
**Process:**
1. **Web Search Enrichment:** Actively performs external web searches on high-interest entities to gather more context, fetch recent developments, and ingest the latest news into the Knowledge Base.
2. **Trend Forecasting:** Synthesizes historical data points within the Wiki to predict modeling trends and generate forecasting reports.
3. **Constant Cleaning:** De-duplicates nodes, prunes broken links, and restructures directories for better organization.
**Outputs:** Appended context on existing pages and newly generated `Forecast_Report.md`.
