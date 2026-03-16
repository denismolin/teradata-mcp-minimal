import os
import re

import teradatasql
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(
    "teradata-mcp-minimal",
    host=os.environ.get("MCP_HOST", "127.0.0.1"),
    port=int(os.environ.get("MCP_PORT", "8000")),
)

_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9_]+$")


def _validate_identifier(name: str) -> str:
    """Raise ValueError if name contains characters unsafe for SQL identifiers."""
    if not _SAFE_IDENTIFIER.match(name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name


def _get_connection() -> teradatasql.TeradataConnection:
    return teradatasql.connect(
        host=os.environ["TD_HOST"],
        user=os.environ["TD_USER"],
        password=os.environ["TD_PASSWORD"],
    )


def _fetch_column(sql: str, params: list | None = None) -> list[str]:
    """Execute sql and return the first column of every row as a list of strings."""
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or [])
            return [str(row[0]).strip() for row in cur.fetchall()]


def _fetch_text(sql: str) -> str:
    """Execute sql and join all rows of the first column into a single string."""
    rows = _fetch_column(sql)
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_databases() -> list[str]:
    """Return the list of all databases visible to the connected user."""
    return _fetch_column(
        "SELECT DatabaseName FROM DBC.DatabasesV ORDER BY 1"
    )


@mcp.tool()
def list_tables(database: str) -> list[str]:
    """Return the list of tables in the given database."""
    _validate_identifier(database)
    return _fetch_column(
        "SELECT TableName FROM DBC.TablesV "
        "WHERE DatabaseName=? AND TableKind='T' ORDER BY 1",
        [database],
    )


@mcp.tool()
def list_views(database: str) -> list[str]:
    """Return the list of views in the given database."""
    _validate_identifier(database)
    return _fetch_column(
        "SELECT TableName FROM DBC.TablesV "
        "WHERE DatabaseName=? AND TableKind='V' ORDER BY 1",
        [database],
    )


@mcp.tool()
def get_object_type(database: str, object_name: str) -> str:
    """Return whether the object is a TABLE or a VIEW (or UNKNOWN if not found)."""
    _validate_identifier(database)
    _validate_identifier(object_name)
    rows = _fetch_column(
        "SELECT TableKind FROM DBC.TablesV "
        "WHERE DatabaseName=? AND TableName=?",
        [database, object_name],
    )
    if not rows:
        return "UNKNOWN"
    kind = rows[0]
    return {"T": "TABLE", "V": "VIEW"}.get(kind, kind)


@mcp.tool()
def get_table_ddl(database: str, table_name: str) -> str:
    """Return the DDL (CREATE TABLE statement) for the given table."""
    _validate_identifier(database)
    _validate_identifier(table_name)
    return _fetch_text(f"SHOW TABLE {database}.{table_name}")


@mcp.tool()
def get_view_ddl(database: str, view_name: str) -> str:
    """Return the DDL (CREATE VIEW statement) for the given view."""
    _validate_identifier(database)
    _validate_identifier(view_name)
    return _fetch_text(f"SHOW VIEW {database}.{view_name}")


@mcp.tool()
def get_query_explain(query: str) -> str:
    """Return the Teradata explain plan for the given SQL query."""
    return _fetch_text(f"EXPLAIN {query}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
