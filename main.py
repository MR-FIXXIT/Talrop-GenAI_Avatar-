import chromadb
from chromadb.utils import embedding_functions
import os
import hashlib


def get_chroma_client():
    """
    Initialize and return ChromaDB client with default embedding function.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    default_ef = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=default_ef,
        metadata={"description": "Document embeddings collection"}
    )

    return collection


def read_text_file(file_path: str) -> str:
    """
    Read content from a text file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_doc_id(file_path: str) -> str:
    """
    Generate a unique document ID based on file path.
    """
    return hashlib.md5(file_path.encode()).hexdigest()


def embed_single_file(collection, file_path: str) -> bool:
    """
    Embed a single text file into the collection.
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            return False

        content = read_text_file(file_path)
        doc_id = generate_doc_id(file_path)
        file_name = os.path.basename(file_path)

        # Check if document already exists
        existing = collection.get(ids=[doc_id])
        if existing['ids']:
            print(f"Updating existing document: {file_name}")
            collection.update(
                ids=[doc_id],
                documents=[content],
                metadatas=[{"source": file_path, "filename": file_name}]
            )
        else:
            print(f"Adding new document: {file_name}")
            collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[{"source": file_path, "filename": file_name}]
            )

        return True
    except Exception as e:
        print(f"Error embedding file {file_path}: {e}")
        return False


def embed_files_from_directory(collection, directory_path: str, extensions: list = None) -> int:
    """
    Embed all text files from a directory.

    Args:
        collection: ChromaDB collection
        directory_path: Path to the directory containing text files
        extensions: List of file extensions to include (e.g., ['.txt', '.md'])
                   If None, defaults to ['.txt']

    Returns:
        Number of files successfully embedded
    """
    if extensions is None:
        extensions = ['.txt']

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found - {directory_path}")
        return 0

    success_count = 0

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                if embed_single_file(collection, file_path):
                    success_count += 1

    print(f"\nSuccessfully embedded {success_count} file(s)")
    print(f"Total documents in collection: {collection.count()}")

    return success_count


def embed_files_from_list(collection, file_paths: list) -> int:
    """
    Embed multiple files from a list of file paths.

    Args:
        collection: ChromaDB collection
        file_paths: List of file paths to embed

    Returns:
        Number of files successfully embedded
    """
    success_count = 0

    for file_path in file_paths:
        if embed_single_file(collection, file_path):
            success_count += 1

    print(f"\nSuccessfully embedded {success_count} out of {len(file_paths)} file(s)")
    print(f"Total documents in collection: {collection.count()}")

    return success_count


def interactive_file_upload(collection):
    """
    Interactive mode for uploading files.
    """
    print("\n" + "=" * 50)
    print("ChromaDB Document Embedding - Interactive Mode")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Upload a single file")
        print("2. Upload all files from a directory")
        print("3. Query documents")
        print("4. Show collection stats")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            file_path = input("Enter the file path: ").strip().strip('"')
            embed_single_file(collection, file_path)

        elif choice == "2":
            dir_path = input("Enter the directory path: ").strip().strip('"')
            ext_input = input("Enter file extensions (comma-separated, e.g., .txt,.md) or press Enter for .txt: ").strip()

            if ext_input:
                extensions = [ext.strip() for ext in ext_input.split(',')]
            else:
                extensions = ['.txt']

            embed_files_from_directory(collection, dir_path, extensions)

        elif choice == "3":
            query = input("Enter your search query: ").strip()
            if query:
                n_results = input("Number of results (default 3): ").strip()
                n_results = int(n_results) if n_results.isdigit() else 3
                query_documents(collection, query, n_results)

        elif choice == "4":
            print(f"\nTotal documents in collection: {collection.count()}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


def query_documents(collection, query_text, n_results=5):
    """
    Query the collection to find similar documents.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    print(f"\nQuery: '{query_text}'")
    print("=" * 50)

    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        print(f"\n{i+1}. Document: {doc}")
        print(f"   Metadata: {metadata}")
        print(f"   Distance: {distance:.4f}")

    return results


def main():
    # Initialize ChromaDB collection
    collection = get_chroma_client()

    print(f"ChromaDB initialized. Current document count: {collection.count()}")

    # Run interactive mode for file uploads
    interactive_file_upload(collection)


if __name__ == "__main__":
    main()

