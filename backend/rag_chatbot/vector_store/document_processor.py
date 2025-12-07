import os
import markdown
from pathlib import Path
from typing import List, Dict, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..config import settings


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )

    def process_textbook_content(self, docs_path: str = "frontend/docusaurus/docs"):
        """Process all textbook markdown files and extract content with metadata"""
        documents = []

        for root, dirs, files in os.walk(docs_path):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, docs_path)

                    # Extract content and metadata from the file
                    content, metadata = self._extract_content_with_metadata(file_path, relative_path)

                    # Split content into chunks
                    chunks = self.text_splitter.split_text(content)

                    # Create document objects with metadata
                    for i, chunk in enumerate(chunks):
                        doc_metadata = metadata.copy()
                        doc_metadata["chunk_id"] = f"{relative_path}_chunk_{i}"
                        doc_metadata["chunk_index"] = i
                        doc_metadata["total_chunks"] = len(chunks)

                        documents.append({
                            "content": chunk,
                            "metadata": doc_metadata
                        })

        return documents

    def _extract_content_with_metadata(self, file_path: str, relative_path: str) -> Tuple[str, Dict]:
        """Extract content and metadata from a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from file path
        path_parts = relative_path.replace('.mdx', '').replace('.md', '').split('/')
        metadata = {
            "source_file": relative_path,
            "part": path_parts[0] if len(path_parts) > 0 else "unknown",
            "chapter": path_parts[1] if len(path_parts) > 1 else "unknown",
            "section": path_parts[2] if len(path_parts) > 2 else "unknown",
            "full_path": relative_path
        }

        # Remove frontmatter if present (common in Docusaurus docs)
        if content.startswith('---'):
            end_frontmatter = content.find('---', 3)
            if end_frontmatter != -1:
                content = content[end_frontmatter + 3:].strip()

        # Convert markdown to plain text while preserving some structure
        html = markdown.markdown(content)
        # Simple conversion to plain text (in a real implementation, you might want a more sophisticated approach)
        plain_text = self._html_to_text(html)

        return plain_text, metadata

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text while preserving structure"""
        import re

        # Remove script and style elements
        html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)

        # Replace headers with plain text indicators
        html = re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>', r'\n\2\n', html)

        # Replace list items with plain text indicators
        html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html)

        # Replace paragraphs with newlines
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html)

        # Replace links with text and URL
        html = re.sub(r'<a[^>]*href=[\'"]([^\'"]*)[\'"][^>]*>(.*?)</a>', r'\2 (\1)', html)

        # Remove other HTML tags
        html = re.sub(r'<[^>]+>', '', html)

        # Clean up extra whitespace
        html = re.sub(r'\n\s*\n', '\n\n', html)

        return html.strip()

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks of appropriate size"""
        return self.text_splitter.split_text(text)