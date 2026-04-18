# Research Output Saver

Shared reference for all research skills (x-research, youtube-research, etc.). After presenting results to the user, save the output to `docs/research/`.

## Save rules

1. Determine the topic slug from the research question. Use lowercase, hyphens, no dates. Examples:
   - "How do people use Claude Code?" -> `using-claude-code-workflows`
   - "Best MCP servers for Claude Code" -> `mcp-servers-claude-code`
   - "What devs say about Cursor vs Copilot" -> `cursor-vs-copilot`

2. Check if a topic folder already exists under `docs/research/` that fits. Scan existing folders and files:
   ```bash
   ls docs/research/
   ```
   - If a matching folder exists (e.g. `claude-code/`), save inside it.
   - If no matching folder exists, create one with a short category name.
   - If the research does not fit any category, save directly in `docs/research/`.

3. Check for existing files that overlap with this research. If a file covers the same topic, update it rather than creating a duplicate.

4. Save the file as `docs/research/<category>/<topic-slug>.md`. The file contains only the output table and sources. No frontmatter. No metadata beyond what the output format already includes.

## Folder organisation

When saving, review existing files in `docs/research/` and reorganise if needed:
- Group related files into topic folders (e.g. all Claude Code research into `claude-code/`)
- Move orphaned files into the right folder if one now exists
- Keep folder names short: `claude-code`, `marketing`, `tools`, not `claude-code-related-research`

## What NOT to save

- Raw sub-agent output (the /tmp/ files). These are ephemeral.
- Duplicate research. If the same question was already researched, update the existing file.
