import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class HealthKnowledgeBase:
    """Loads health coaching documents, embeds them, and serves relevant context via similarity search."""

    def __init__(self, docs_dir: str, persist_dir: str):
        self.docs_dir = Path(docs_dir)
        self.persist_dir = str(persist_dir)
        self.collection_name = "health_coach_kb"
        self._vectorstore: Chroma | None = None

    def _get_embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(model="text-embedding-3-small")

    def load(self) -> None:
        """Load from existing ChromaDB if available; otherwise build from documents."""
        embeddings = self._get_embeddings()

        existing = Chroma(
            collection_name=self.collection_name,
            embedding_function=embeddings,
            persist_directory=self.persist_dir,
        )

        # If the collection already has documents, reuse it
        if existing._collection.count() > 0:
            self._vectorstore = existing
            return

        # First run: load, chunk, embed, and persist
        self._build_index(embeddings)

    def _build_index(self, embeddings: OpenAIEmbeddings) -> None:
        loader = DirectoryLoader(
            str(self.docs_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=False,
        )
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " "],
        )
        chunks = splitter.split_documents(documents)

        self._vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_dir,
        )

    def retrieve(self, query: str, k: int = 3) -> str:
        """Return top-k relevant knowledge chunks as a single formatted string."""
        if self._vectorstore is None:
            return ""

        results = self._vectorstore.similarity_search(query, k=k)
        if not results:
            return ""

        sections = []
        for i, doc in enumerate(results, 1):
            source = Path(doc.metadata.get("source", "knowledge")).stem.replace("_", " ").title()
            sections.append(f"[{source}]\n{doc.page_content.strip()}")

        return "\n\n---\n\n".join(sections)
