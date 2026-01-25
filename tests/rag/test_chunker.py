from rag.chunker import chunk_text


def test_chunk_text():
    text = "word " * 1000
    chunks = chunk_text(text, chunk_size=100, overlap=10)

    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)
