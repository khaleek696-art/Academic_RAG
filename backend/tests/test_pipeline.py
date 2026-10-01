import unittest
from backend.app.services.chunker import PageAwareChunker

class TestRAGPipeline(unittest.TestCase):
    def test_chunker_initialization(self):
        chunker = PageAwareChunker(chunk_size=500, chunk_overlap=50)
        self.assertEqual(chunker.chunk_size, 500)
        self.assertEqual(chunker.chunk_overlap, 50)

if __name__ == '__main__':
    unittest.main()
