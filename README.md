# teradata-mcp-minimal

A minimal [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for Teradata Vantage. Exposes metadata-only tools — no data queries are executed.

## Tools

| Tool | Description |
|---|---|
| `list_databases` | List all databases visible to the connected user |
| `list_tables(database)` | List tables in a database |
| `list_views(database)` | List views in a database |
| `get_object_type(database, object_name)` | Returns `TABLE`, `VIEW`, or `UNKNOWN` |
| `get_table_ddl(database, table_name)` | DDL for a table (`SHOW TABLE`) |
| `get_view_ddl(database, view_name)` | DDL for a view (`SHOW VIEW`) |
| `get_query_explain(query)` | Execution plan for a query (`EXPLAIN`) |

## Requirements

- Python 3.10+
- Teradata Vantage instance accessible from the host

## Installation

```bash
pip install -e .
```

## Configuration

Copy `.env.example` and set your connection parameters:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `TD_HOST` | Teradata server hostname or IP |
| `TD_USER` | Database username |
| `TD_PASSWORD` | Database password |

## Running

```bash
export TD_HOST=your-host TD_USER=your-user TD_PASSWORD=your-password
python server.py
```

Or using the installed entry point:

```bash
teradata-mcp
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
        "TD_HOST": "your-host",
        "TD_USER": "your-user",
        "TD_PASSWORD": "your-password"
      }
    }
  }
}
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```
