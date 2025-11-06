#!/usr/bin/env python3
"""
Generate semantic embeddings for text summaries.
"""

import numpy as np
from typing import List

# Try to import sentence_transformers
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    print("Warning: sentence-transformers not available, using TF-IDF fallback")

# Fallback to sklearn TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingGenerator:
    """Generate semantic embeddings for text."""

    def __init__(self, method='sentence-transformer'):
        """
        Initialize embedding generator.

        Args:
            method: 'sentence-transformer' or 'tfidf'
        """
        self.method = method

        if method == 'sentence-transformer':
            if not HAS_SENTENCE_TRANSFORMERS:
                print("Falling back to TF-IDF method")
                self.method = 'tfidf'
                self._init_tfidf()
            else:
                self._init_sentence_transformer()
        elif method == 'tfidf':
            self._init_tfidf()
        else:
            raise ValueError(f"Unknown method: {method}")

    def _init_sentence_transformer(self):
        """Initialize sentence transformer model."""
        print("Loading sentence-transformer model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorizer = None
        print("Model loaded successfully")

    def _init_tfidf(self):
        """Initialize TF-IDF vectorizer."""
        print("Using TF-IDF vectorizer for embeddings")
        self.model = None
        self.vectorizer = TfidfVectorizer(
            max_features=384,  # Match sentence-transformer dimension
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings

        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        if not texts:
            raise ValueError("No texts provided")

        if self.method == 'sentence-transformer':
            return self._generate_sentence_transformer(texts)
        else:
            return self._generate_tfidf(texts)

    def _generate_sentence_transformer(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using sentence transformer."""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def _generate_tfidf(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using TF-IDF."""
        embeddings = self.vectorizer.fit_transform(texts)
        return embeddings.toarray()

    @property
    def embedding_dim(self) -> int:
        """Get embedding dimensionality."""
        if self.method == 'sentence-transformer':
            return self.model.get_sentence_embedding_dimension()
        else:
            return self.vectorizer.max_features
