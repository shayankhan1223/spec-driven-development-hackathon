"""
Agent Tools for the Physical AI & Humanoid Robotics Textbook Assistant
These tools provide specialized functions for the AI agent to use
"""

from typing import Dict, List, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings
from .rag_retriever import RAGRetriever
import asyncio


class AgentTools:
    """
    Collection of specialized tools for the textbook AI agent
    """

    def __init__(self):
        self.rag_retriever = RAGRetriever()

    def search_textbook_content(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Search the Physical AI & Humanoid Robotics textbook for relevant information

        Args:
            query: The search query to find relevant textbook content
            top_k: Number of results to return (default 5)

        Returns:
            Dictionary with search results and metadata
        """
        try:
            results = self.rag_retriever.retrieve(query, top_k=top_k)

            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc["text"],
                    "source_file": doc["metadata"].get("source_file", "unknown"),
                    "page": doc["metadata"].get("page", "unknown"),
                    "section": doc["metadata"].get("section", "unknown"),
                    "relevance_score": doc.get("score", 0.0)
                })

            return {
                "status": "success",
                "query": query,
                "results_count": len(formatted_results),
                "results": formatted_results
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error searching textbook content: {str(e)}",
                "query": query
            }

    def get_chapter_outline(self, chapter_title: str) -> Dict[str, Any]:
        """
        Get the outline of a specific chapter in the textbook

        Args:
            chapter_title: The title or partial title of the chapter

        Returns:
            Dictionary with chapter outline information
        """
        try:
            # This would normally query a structured representation of the textbook
            # For now, we'll search for content related to the chapter
            search_results = self.rag_retriever.retrieve(f"outline {chapter_title}", top_k=3)

            sections = []
            for doc in search_results:
                text = doc["text"]
                # Extract section headers (simple heuristic - could be improved)
                lines = text.split('\n')
                for line in lines:
                    if line.strip().endswith(':') or line.strip().endswith('.') or line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                        sections.append(line.strip())

            # Limit to unique sections and take first 10
            unique_sections = list(dict.fromkeys(sections))[:10]

            return {
                "status": "success",
                "chapter_title": chapter_title,
                "outline": unique_sections
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error getting chapter outline: {str(e)}",
                "chapter_title": chapter_title
            }

    def get_glossary_terms(self, terms: List[str]) -> Dict[str, Any]:
        """
        Get definitions for specific terms from the textbook glossary

        Args:
            terms: List of terms to look up in the glossary

        Returns:
            Dictionary with term definitions
        """
        try:
            glossary_results = {}

            for term in terms:
                # Search for the term in the textbook
                search_results = self.rag_retriever.retrieve(f"definition of {term}", top_k=1)

                if search_results:
                    definition = search_results[0]["text"]
                    glossary_results[term] = {
                        "term": term,
                        "definition": definition,
                        "source": search_results[0]["metadata"].get("source_file", "unknown")
                    }
                else:
                    glossary_results[term] = {
                        "term": term,
                        "definition": f"Definition for '{term}' not found in the textbook",
                        "source": "unknown"
                    }

            return {
                "status": "success",
                "terms": glossary_results
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error getting glossary terms: {str(e)}",
                "terms": {term: {"error": str(e)} for term in terms}
            }

    def get_related_concepts(self, concept: str) -> Dict[str, Any]:
        """
        Find related concepts to a given concept in the textbook

        Args:
            concept: The concept to find related concepts for

        Returns:
            Dictionary with related concepts
        """
        try:
            # Search for content related to the concept
            search_results = self.rag_retriever.retrieve(f"related to {concept}", top_k=5)

            related_concepts = set()
            for doc in search_results:
                text = doc["text"].lower()
                # Simple approach: extract capitalized words that might be concepts
                words = text.split()
                for word in words:
                    word = word.strip('.,;:!?()[]{}"\'')
                    if len(word) > 3 and word[0].isupper() and word not in ['The', 'And', 'For', 'With', 'This', 'That', 'These', 'Those']:
                        related_concepts.add(word)

            return {
                "status": "success",
                "concept": concept,
                "related_concepts": list(related_concepts)[:10]  # Limit to 10 concepts
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error getting related concepts: {str(e)}",
                "concept": concept
            }

    def explain_application(self, concept: str) -> Dict[str, Any]:
        """
        Explain practical applications of a given concept in the textbook

        Args:
            concept: The concept to explain applications for

        Returns:
            Dictionary with applications of the concept
        """
        try:
            # Search for applications of the concept
            search_results = self.rag_retriever.retrieve(f"application of {concept} in robotics", top_k=3)

            applications = []
            for doc in search_results:
                applications.append({
                    "application": doc["text"][:500] + "..." if len(doc["text"]) > 500 else doc["text"],
                    "source": doc["metadata"].get("source_file", "unknown"),
                    "context": doc["metadata"].get("section", "unknown")
                })

            return {
                "status": "success",
                "concept": concept,
                "applications": applications
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Error explaining applications: {str(e)}",
                "concept": concept
            }

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Return all available tools in OpenAI function format
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_textbook_content",
                    "description": "Search the Physical AI & Humanoid Robotics textbook for relevant information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find relevant textbook content"
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of results to return (default 5)",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_chapter_outline",
                    "description": "Get the outline of a specific chapter in the textbook",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chapter_title": {
                                "type": "string",
                                "description": "The title or partial title of the chapter to get outline for"
                            }
                        },
                        "required": ["chapter_title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_glossary_terms",
                    "description": "Get definitions for specific terms from the textbook glossary",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "terms": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "List of terms to look up in the glossary"
                            }
                        },
                        "required": ["terms"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_related_concepts",
                    "description": "Find related concepts to a given concept in the textbook",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "concept": {
                                "type": "string",
                                "description": "The concept to find related concepts for"
                            }
                        },
                        "required": ["concept"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "explain_application",
                    "description": "Explain practical applications of a given concept in the textbook",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "concept": {
                                "type": "string",
                                "description": "The concept to explain applications for"
                            }
                        },
                        "required": ["concept"]
                    }
                }
            }
        ]