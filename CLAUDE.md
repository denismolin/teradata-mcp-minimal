# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

`teradata-mcp-minimal` is a minimal [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server implementation for Teradata. It is intended to expose Teradata database capabilities (query execution, schema inspection, etc.) to MCP-compatible AI clients.

## Technology Stack

- **Language:** Python
- **MCP SDK:** [`mcp`](https://github.com/modelcontextprotocol/python-sdk)
- **Teradata driver:** [`teradatasql`](https://pypi.org/project/teradatasql/) (preferred)
- **SQL dialect:** Teradata SQL — always generate/validate SQL using Teradata syntax (e.g., `SEL` shorthand, `TOP n` instead of `LIMIT`, `QUALIFY`, `CAST` with Teradata types, BTEQ-style constructs where relevant)

## Architecture

Single-file server (`server.py`) using `FastMCP` (stdio transport). One connection per tool call — no pooling. All tools operate on Teradata metadata only (DBC views, SHOW, EXPLAIN); no data queries are executed.

Identifier inputs to SHOW statements are validated against `^[A-Za-z0-9_]+$` before interpolation, since `teradatasql` does not support parameters for DDL statements.

### Tools

| Tool | Description |
|---|---|
| `list_databases` | All databases visible to the connected user |
| `list_tables(database)` | Tables in a database (`DBC.TablesV`, `TableKind='T'`) |
| `list_views(database)` | Views in a database (`DBC.TablesV`, `TableKind='V'`) |
| `get_object_type(database, object_name)` | Returns `TABLE`, `VIEW`, or `UNKNOWN` |
| `get_table_ddl(database, table_name)` | `SHOW TABLE db.name` |
| `get_view_ddl(database, view_name)` | `SHOW VIEW db.name` |
| `get_query_explain(query)` | `EXPLAIN <query>` |

## Setup

```bash
pip install -e .
```

Required environment variables (see `.env.example`):

```
TD_HOST=your-teradata-host
TD_USER=your-username
TD_PASSWORD=your-password
```

## Running

```bash
# Direct
python server.py

# Via installed entry point
teradata-mcp
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Claude Desktop integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "teradata": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "TD_HOST": "...",
        "TD_USER": "...",
        "TD_PASSWORD": "..."
      }
    }
  }
}
```
