import sys
import asyncio
from pathlib import Path

from rag.ingest import ingest_document

USAGE = """
Usage:
python ingest_docs.py <tenant_id> <file_or_directory>
"""


async def main():
    if len(sys.argv) < 3:
        print(USAGE)
        return

    tenant_id = sys.argv[1]
    path = Path(sys.argv[2])

    if path.is_file():
        text = path.read_text()
        await ingest_document(tenant_id, text, source=path.name)
        print(f"✅ Ingested {path.name}")

    elif path.is_dir():
        for file in path.glob("*.txt"):
            text = file.read_text()
            await ingest_document(tenant_id, text, source=file.name)
            print(f"✅ Ingested {file.name}")

    else:
        print("❌ Invalid path")


if __name__ == "__main__":
    asyncio.run(main())
