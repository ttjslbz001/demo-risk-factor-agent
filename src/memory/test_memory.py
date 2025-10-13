"""
Mem0 AI Memory Layer
This module provides a wrapper around mem0ai for managing AI agent memory.
"""

import os
from typing import Optional, Dict, List, Any
from mem0 import Memory


class MemoryLayer:
    """
    A memory management layer using mem0ai for storing and retrieving
    agent memories, conversations, and contextual information.
    """
    
    def __init__(
        self,
        llm_provider: str = "openai",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ):
        """
        Initialize the Memory Layer with configuration.
        
        Args:
            llm_provider: The LLM provider to use (e.g., "openai", "groq", "ollama")
            model: The model name to use
            api_key: API key for the LLM provider (if not set via environment variable)
            temperature: Temperature setting for the LLM
            max_tokens: Maximum tokens for generation
            **kwargs: Additional provider-specific configuration
        """

        os.environ["OPENAI_API_KEY"] = "sk-nIDrG5iv1XNwFzRcaAzDgg"
   
        
        # Build the configuration
        self.config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o",
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "openai_base_url": "https://us-ailab-api.telenav.com/v1",
                    "api_key": "sk-nIDrG5iv1XNwFzRcaAzDgg",
     
                    **kwargs
                }
            },
           "embedder": {
                "provider": "openai",
                "config": {
                    "model": "ailab-embedding",
                    "openai_base_url": "https://us-ailab-api.telenav.com/v1",
                },
            },
           "vector_store": {
                "vector_store": {
                "provider": "milvus",
                "config": {
                    "collection_name": "quickstart_mem0_with_milvus",
                    "embedding_model_dims": "1536",
                    "url": "./milvus.db",  # Use local vector database for demo purpose
                },
    },
            }
    }
        
        # Initialize memory instance
        self.memory = Memory.from_config(self.config)
        
    def add_memory(
        self,
        text: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a new memory to the system.
        
        Args:
            text: The text content to store
            user_id: User identifier for user-specific memories
            agent_id: Agent identifier for agent-specific memories
            run_id: Run identifier for session-specific memories
            metadata: Additional metadata to store with the memory
            
        Returns:
            Dictionary containing the result of the add operation
        """
        kwargs = {}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        if metadata:
            kwargs["metadata"] = metadata
            
        result = self.memory.add(text, **kwargs)
        return result
    
    def get_memories(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories based on identifiers.
        
        Args:
            user_id: User identifier to filter by
            agent_id: Agent identifier to filter by
            run_id: Run identifier to filter by
            limit: Maximum number of memories to return
            
        Returns:
            List of memory dictionaries
        """
        kwargs = {}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        if limit:
            kwargs["limit"] = limit
            
        memories = self.memory.get_all(**kwargs)
        return memories
    
    def search_memories(
        self,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search memories using semantic search.
        
        Args:
            query: Search query text
            user_id: User identifier to filter by
            agent_id: Agent identifier to filter by
            run_id: Run identifier to filter by
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memory dictionaries
        """
        kwargs = {"limit": limit}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
            
        results = self.memory.search(query, **kwargs)
        return results
    
    def update_memory(
        self,
        memory_id: str,
        text: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing memory.
        
        Args:
            memory_id: The ID of the memory to update
            text: New text content
            user_id: User identifier
            agent_id: Agent identifier
            run_id: Run identifier
            metadata: Updated metadata
            
        Returns:
            Dictionary containing the result of the update operation
        """
        kwargs = {"memory_id": memory_id}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        if metadata:
            kwargs["metadata"] = metadata
            
        result = self.memory.update(text, **kwargs)
        return result
    
    def delete_memory(
        self,
        memory_id: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete a specific memory.
        
        Args:
            memory_id: The ID of the memory to delete
            user_id: User identifier
            agent_id: Agent identifier
            run_id: Run identifier
            
        Returns:
            Dictionary containing the result of the delete operation
        """
        kwargs = {"memory_id": memory_id}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
            
        result = self.memory.delete(**kwargs)
        return result
    
    def delete_all_memories(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete all memories for a given identifier.
        
        Args:
            user_id: User identifier
            agent_id: Agent identifier
            run_id: Run identifier
            
        Returns:
            Dictionary containing the result of the delete operation
        """
        kwargs = {}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
            
        result = self.memory.delete_all(**kwargs)
        return result
    
    def get_memory_history(
        self,
        memory_id: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get the history of changes for a specific memory.
        
        Args:
            memory_id: The ID of the memory
            user_id: User identifier
            agent_id: Agent identifier
            run_id: Run identifier
            
        Returns:
            List of history entries for the memory
        """
        kwargs = {"memory_id": memory_id}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
            
        history = self.memory.history(**kwargs)
        return history


# Example usage
if __name__ == "__main__":
    # Initialize the memory layer
    # Make sure to set OPENAI_API_KEY in environment or pass it here
    memory_layer = MemoryLayer(
        llm_provider="openai",
        model="gpt-4o",
        temperature=0.7
    )
    
    # Add a memory
    print("Adding memory...")
    result = memory_layer.add_memory(
        text="User prefers Python for backend development and React for frontend.",
        user_id="user_123",
        metadata={"category": "preferences", "timestamp": "2025-10-13"}
    )
    print(f"Memory added: {result}")
    
    # Search memories
    print("\nSearching memories...")
    results = memory_layer.search_memories(
        query="What does the user prefer for development?",
        user_id="user_123",
        limit=5
    )
    print(f"Search results: {results}")
    
    # Get all memories for a user
    print("\nGetting all memories...")
    all_memories = memory_layer.get_memories(user_id="user_123")
    print(f"All memories: {all_memories}")
    
    # Update a memory (example - you'd need the actual memory_id from the add result)
    # memory_layer.update_memory(
    #     memory_id="mem_xyz",
    #     text="User prefers Python with FastAPI for backend and React with TypeScript for frontend.",
    #     user_id="user_123"
    # )
    
    # Delete a specific memory
    # memory_layer.delete_memory(memory_id="mem_xyz", user_id="user_123")
    
    # Delete all memories for a user
    # memory_layer.delete_all_memories(user_id="user_123")

