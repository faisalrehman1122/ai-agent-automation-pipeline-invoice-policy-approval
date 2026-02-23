from typing import Dict, Any, List, Optional

class PolicyTool:
    def __init__(self):
        self.policy_text: Optional[str] = None
        self.chunks: List[str] = []

    def store_policy(self, text: str) -> Dict[str, Any]:
        self.policy_text = text
        self.chunks = self._split_into_chunks(text)
        return {
            "status": "success",
            "chunks_count": len(self.chunks),
            "message": f"Policy stored with {len(self.chunks)} chunks"
        }

    def _split_into_chunks(self, text: str, chunk_size: int = 200) -> List[str]:
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    def retrieve(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        if not self.policy_text:
            return {
                "status": "error",
                "message": "No policy text stored"
            }

        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_chunks = []
        for idx, chunk in enumerate(self.chunks):
            chunk_lower = chunk.lower()
            chunk_words = set(chunk_lower.split())
            
            matches = len(query_words.intersection(chunk_words))
            score = matches / len(query_words) if query_words else 0
            
            if score > 0:
                scored_chunks.append({
                    "chunk_id": idx,
                    "text": chunk,
                    "score": round(score, 3),
                    "matches": matches
                })
        
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        top_chunks = scored_chunks[:top_k]
        
        return {
            "status": "success",
            "query": query,
            "results": top_chunks,
            "count": len(top_chunks)
        }

    def cite(self, claim: str) -> Dict[str, Any]:
        result = self.retrieve(claim, top_k=2)
        if result["status"] == "success" and result["results"]:
            citations = [
                {
                    "text": chunk["text"],
                    "relevance_score": chunk["score"]
                }
                for chunk in result["results"]
            ]
            return {
                "status": "success",
                "claim": claim,
                "citations": citations
            }
        return {
            "status": "no_citations",
            "claim": claim,
            "message": "No relevant policy chunks found"
        }
