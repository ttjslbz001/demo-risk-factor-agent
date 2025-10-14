"""
Product Definition Agent - Fully Memory-Driven (mem0) Agent

This agent is responsible for:
1. Defining required risk factors for products
2. Providing risk factor definitions <risk_subject, risk_factor_name>[]
3. Supplying assessment rules for each risk factor
4. Maintaining product-specific rule configurations
5. Defining how risk factors should be evaluated

🔥 FULLY MEMORY-DRIVEN ARCHITECTURE:
- NO hardcoded product definitions - everything loaded from mem0
- NO local state management - all data retrieved dynamically
- Persistent knowledge storage in mem0 vector database
- Learning from interactions and usage patterns
- Context-aware responses using semantic search
- Growing knowledge base over time
- Stateless agent design for scalability

To initialize the memory with products, use:
    python bootstrap_product_memory.py --sample-data
"""

import logging
from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

from src.utils.rule_loader import load_rules
from src.gateway.agent_factory import init_agent
from src.memory.test_memory import MemoryLayer

logger = logging.getLogger(__name__)


@dataclass
class RiskFactorDefinition:
    """Definition of a risk factor for a product."""
    risk_subject: str  # e.g., "driver", "vehicle", "policy"
    risk_factor_name: str  # e.g., "three_year_claim_free_discount"
    description: str
    evaluation_rules: List[str]
    required: bool = True
    weight: float = 1.0


@dataclass
class ProductDefinition:
    """Complete product definition with risk factors and rules."""
    product_code: str
    product_name: str
    risk_factors: List[RiskFactorDefinition]
    assessment_rules: Dict[str, Any]
    coverage_options: Dict[str, Any]


class ProductDefinitionAgent:
    """
    Fully memory-driven agent responsible for defining products, risk factors, and assessment rules.
    
    🔥 STATELESS ARCHITECTURE - All data loaded from mem0:
    - Store and retrieve product definitions from mem0 vector database
    - NO local caching - queries mem0 for every request
    - Learn from interactions and store insights in mem0
    - Provide context-aware responses using semantic search
    - Dynamically growing knowledge base
    - Horizontally scalable stateless design
    """
    
    def __init__(
        self, 
        rules_dir: str = "docs/insurance_risk_factor_agent/3_year_claim_free_discount",
        use_memory: bool = True,
        agent_id: str = "product_definition_agent",
        user_id: str = "user_123"
    ):
        """
        Initialize the memory-based product definition agent.
        
        Args:
            rules_dir: Directory containing product rules
            use_memory: Enable memory-based learning (default: True)
            agent_id: Unique identifier for this agent
            user_id: User/system identifier for memory isolation
        """
        # Initialize LLM agent (optional - graceful degradation if not available)
        try:
            self.agent = init_agent()
            logger.info("LLM agent initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize LLM agent: {e}. Agent will work with limited functionality.")
            self.agent = None
        
        self.rules_dir = rules_dir
        self.agent_id = agent_id
        self.user_id = user_id
        self.use_memory = use_memory
        
        # Initialize memory layer if enabled
        if self.use_memory:
            try:
                self.memory = MemoryLayer(
                    llm_provider="openai",
                    temperature=0.3,
                    max_tokens=4000
                )
                logger.info(f"Memory layer initialized for agent: {agent_id}")
            except Exception as e:
                logger.warning(f"Failed to initialize memory layer: {e}. Running without memory.")
                self.use_memory = False
                self.memory = None
        else:
            self.memory = None
        
        logger.info("ProductDefinitionAgent initialized - all data loaded dynamically from mem0")
            
    def _parse_product_from_memory(self, memory_result: Dict[str, Any]) -> Optional[ProductDefinition]:
        """
        Parse a product definition from a memory search result.
        
        Args:
            memory_result: Memory search result containing product information
            
        Returns:
            ProductDefinition if successfully parsed, None otherwise
        """
        try:
            import json
            
            # Extract text from memory result
            if isinstance(memory_result, dict):
                text = memory_result.get('memory', memory_result.get('text', ''))
                metadata = memory_result.get('metadata', {})
            else:
                text = str(memory_result)
                metadata = {}
            
            # Try to parse as JSON first
            try:
                # Look for JSON structure in text
                if '{' in text and '}' in text:
                    # Extract JSON portion
                    start_idx = text.find('{')
                    end_idx = text.rfind('}') + 1
                    json_str = text[start_idx:end_idx]
                    data = json.loads(json_str)
                    
                    # Build product definition from parsed data
                    if 'product_code' in data or 'productCode' in data:
                        return self._build_product_from_dict(data)
            except json.JSONDecodeError:
                pass
            
            # Try to parse structured text format
            return self._parse_structured_text(text, metadata)
            
        except Exception as e:
            logger.debug(f"Could not parse product from memory: {e}")
            return None
    
    def _build_product_from_dict(self, data: Dict[str, Any]) -> Optional[ProductDefinition]:
        """Build ProductDefinition from dictionary data."""
        try:
            product_code = data.get('product_code') or data.get('productCode')
            product_name = data.get('product_name') or data.get('productName') or product_code
            
            # Parse risk factors
            risk_factors = []
            risk_factors_data = data.get('risk_factors') or data.get('riskFactors') or []
            for rf_data in risk_factors_data:
                risk_factor = RiskFactorDefinition(
                    risk_subject=rf_data.get('risk_subject') or rf_data.get('riskSubject', 'unknown'),
                    risk_factor_name=rf_data.get('risk_factor_name') or rf_data.get('riskFactorName', ''),
                    description=rf_data.get('description', ''),
                    evaluation_rules=rf_data.get('evaluation_rules') or rf_data.get('evaluationRules', []),
                    required=rf_data.get('required', True),
                    weight=rf_data.get('weight', 1.0)
                )
                risk_factors.append(risk_factor)
            
            # Parse assessment rules and coverage options
            assessment_rules = data.get('assessment_rules') or data.get('assessmentRules') or {}
            coverage_options = data.get('coverage_options') or data.get('coverageOptions') or {}
            
            return ProductDefinition(
                product_code=product_code,
                product_name=product_name,
                risk_factors=risk_factors,
                assessment_rules=assessment_rules,
                coverage_options=coverage_options
            )
        except Exception as e:
            logger.debug(f"Could not build product from dict: {e}")
            return None
    
    def _parse_structured_text(self, text: str, metadata: Dict[str, Any]) -> Optional[ProductDefinition]:
        """Parse product definition from structured text format."""
        # This is a fallback parser for text-based product definitions
        # Returns None if the text doesn't look like a product definition
        
        text_lower = text.lower()
        if 'product' not in text_lower:
            return None
        
        # Extract basic info using simple heuristics
        # This is intentionally simple - real data should be in JSON format
        product_code = metadata.get('product_code')
        if not product_code:
            # Try to extract from text
            for line in text.split('\n'):
                if 'product_code' in line.lower() or 'product code' in line.lower():
                    parts = line.split(':')
                    if len(parts) > 1:
                        product_code = parts[1].strip().strip('"').strip("'")
                        break
        
        if not product_code:
            return None
        
        # Build minimal product definition
        return ProductDefinition(
            product_code=product_code,
            product_name=metadata.get('product_name', product_code),
            risk_factors=[],
            assessment_rules={},
            coverage_options={}
        )
        
    def store_product_to_memory(self, product: ProductDefinition) -> bool:
        """
        Store a product definition to memory.
        
        Args:
            product: ProductDefinition to store
            
        Returns:
            Success status
        """
        if not self.use_memory or not self.memory:
            logger.warning("Memory not enabled, cannot store product")
            return False
        
        try:
            import json
            
            # Convert product to dictionary
            product_dict = {
                "product_code": product.product_code,
                "product_name": product.product_name,
                "risk_factors": [
                    {
                        "risk_subject": rf.risk_subject,
                        "risk_factor_name": rf.risk_factor_name,
                        "description": rf.description,
                        "evaluation_rules": rf.evaluation_rules,
                        "required": rf.required,
                        "weight": rf.weight
                    }
                    for rf in product.risk_factors
                ],
                "assessment_rules": product.assessment_rules,
                "coverage_options": product.coverage_options
            }
            
            # Store as JSON in memory
            text = f"Product Definition: {product.product_name}\n{json.dumps(product_dict, indent=2)}"
            
            self.memory.add_memory(
                text=text,
                user_id=self.user_id,
                agent_id=self.agent_id,
                run_id=f"product_def_{datetime.now().strftime('%Y%m%d')}",
                metadata={
                    "category": "product_definition",
                    "product_code": product.product_code,
                    "product_name": product.product_name,
                    "type": "definition",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            logger.info(f"Stored product definition to mem0: {product.product_code}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing product to memory: {e}")
            return False
    
    def load_product_from_rules_dir(self, product_code: str, rules_dir: str) -> Optional[ProductDefinition]:
        """
        Load a product definition from rules directory and store to memory.
        
        Args:
            product_code: Product code to create
            rules_dir: Directory containing rule files
            
        Returns:
            ProductDefinition if successfully loaded and stored
        """
        try:
            rules = load_rules(rules_dir)
            
            # Create product definition from rules
            # This is a bootstrap method to migrate from file-based to memory-based
            product = ProductDefinition(
                product_code=product_code,
                product_name=f"{product_code} Package",
                risk_factors=[],
                assessment_rules={rule["id"]: rule for rule in rules},
                coverage_options={}
            )
            
            # Store to memory
            if self.store_product_to_memory(product):
                logger.info(f"Loaded and stored product from rules: {product_code}")
                return product
            
            return None
            
        except Exception as e:
            logger.error(f"Error loading product from rules directory: {e}")
            return None
    
    def get_product_definition(self, product_code: str) -> Optional[ProductDefinition]:
        """
        Get the complete product definition for a given product code from mem0.
        
        Args:
            product_code: The product code (e.g., "Monthly-Comfort")
            
        Returns:
            ProductDefinition if found in mem0, None otherwise
        """
        if not self.use_memory or not self.memory:
            logger.warning("Memory not enabled, cannot retrieve product definition")
            return None
        
        try:
            # Query mem0 for product definition
            query = f"product definition for {product_code}"
            results = self.memory.search_memories(
                query=query,
                user_id=self.user_id,
                agent_id=self.agent_id,
                limit=5
            )
            
            # Parse and return first matching product
            for result in results:
                product = self._parse_product_from_memory(result)
                if product and product.product_code == product_code:
                    logger.info(f"Retrieved product from mem0: {product_code}")
                    return product
            
            logger.warning(f"Product not found in mem0: {product_code}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading product from mem0: {e}")
            return None
        
    def get_risk_factor_definitions(self, product_code: str) -> List[Tuple[str, str]]:
        """
        Get risk factor definitions as <risk_subject, risk_factor_name> pairs.
        
        Args:
            product_code: The product code
            
        Returns:
            List of (risk_subject, risk_factor_name) tuples
        """
        product = self.get_product_definition(product_code)
        if not product:
            logger.warning(f"Product definition not found: {product_code}")
            return []
            
        return [(rf.risk_subject, rf.risk_factor_name) for rf in product.risk_factors]
        
    def get_assessment_rules(self, product_code: str, risk_factor_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get assessment rules for a product and optionally a specific risk factor.
        
        Args:
            product_code: The product code
            risk_factor_name: Optional specific risk factor name
            
        Returns:
            Dictionary of assessment rules
        """
        product = self.get_product_definition(product_code)
        if not product:
            logger.warning(f"Product definition not found: {product_code}")
            return {}
            
        if risk_factor_name:
            # Filter rules for specific risk factor
            risk_factor = next(
                (rf for rf in product.risk_factors if rf.risk_factor_name == risk_factor_name),
                None
            )
            if risk_factor:
                return {
                    rule_id: product.assessment_rules[rule_id]
                    for rule_id in risk_factor.evaluation_rules
                    if rule_id in product.assessment_rules
                }
            return {}
        
        return product.assessment_rules
        
    def get_coverage_options(self, product_code: str) -> Dict[str, Any]:
        """
        Get coverage options for a product.
        
        Args:
            product_code: The product code
            
        Returns:
            Dictionary of coverage options
        """
        product = self.get_product_definition(product_code)
        if not product:
            logger.warning(f"Product definition not found: {product_code}")
            return {}
            
        return product.coverage_options
        
    def list_available_products(self) -> List[str]:
        """
        Get list of available product codes from mem0.
        
        Returns:
            List of available product codes
        """
        if not self.use_memory or not self.memory:
            logger.warning("Memory not enabled, cannot list products")
            return []
        
        try:
            # Query mem0 for all product definitions
            query = "list all insurance product definitions"
            results = self.memory.search_memories(
                query=query,
                user_id=self.user_id,
                agent_id=self.agent_id,
                limit=50
            )
            
            # Extract unique product codes
            product_codes = set()
            for result in results:
                product = self._parse_product_from_memory(result)
                if product:
                    product_codes.add(product.product_code)
            
            logger.info(f"Found {len(product_codes)} products in mem0")
            return sorted(list(product_codes))
            
        except Exception as e:
            logger.error(f"Error listing products from mem0: {e}")
            return []
        
    def validate_product_configuration(self, product_code: str) -> Dict[str, Any]:
        """
        Validate that a product configuration is complete and valid.
        
        Args:
            product_code: The product code to validate
            
        Returns:
            Validation result with status and issues
        """
        validation_result = {
            "product_code": product_code,
            "valid": False,
            "issues": [],
            "warnings": []
        }
        
        product = self.get_product_definition(product_code)
        if not product:
            validation_result["issues"].append(f"Product definition not found: {product_code}")
            return validation_result
            
        # Check if product has risk factors
        if not product.risk_factors:
            validation_result["issues"].append("No risk factors defined for product")
            
        # Check if all required risk factors have evaluation rules
        for risk_factor in product.risk_factors:
            if risk_factor.required and not risk_factor.evaluation_rules:
                validation_result["issues"].append(
                    f"Required risk factor '{risk_factor.risk_factor_name}' has no evaluation rules"
                )
                
        # Check if assessment rules exist for referenced rule IDs
        for risk_factor in product.risk_factors:
            for rule_id in risk_factor.evaluation_rules:
                if rule_id not in product.assessment_rules:
                    validation_result["warnings"].append(
                        f"Rule '{rule_id}' referenced but not found in assessment rules"
                    )
                    
        validation_result["valid"] = len(validation_result["issues"]) == 0
        
        logger.info(f"Product validation for {product_code}: {'valid' if validation_result['valid'] else 'invalid'}")
        return validation_result
    
    # ==================== Memory-Based Methods ====================
    
    def query_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Query the agent's knowledge base using semantic search.
        
        Args:
            query: Natural language query
            limit: Maximum number of results to return
            
        Returns:
            List of relevant knowledge items with scores
        """
        if not self.use_memory or not self.memory:
            logger.warning("Memory not enabled, cannot query knowledge")
            return []
        
        try:
            results = self.memory.search_memories(
                query=query,
                user_id=self.user_id,
                agent_id=self.agent_id,
                limit=limit
            )
            
            # Normalize results format
            normalized = []
            for result in results:
                if isinstance(result, dict):
                    normalized.append({
                        "text": result.get('memory', result.get('text', str(result))),
                        "score": result.get('score', 0.0),
                        "metadata": result.get('metadata', {})
                    })
                else:
                    normalized.append({
                        "text": str(result),
                        "score": 0.0,
                        "metadata": {}
                    })
            
            logger.info(f"Found {len(normalized)} knowledge items for query: '{query}'")
            return normalized
            
        except Exception as e:
            logger.error(f"Error querying knowledge: {e}")
            return []
    
    def learn_from_interaction(self, interaction_type: str, data: Dict[str, Any]) -> bool:
        """
        Learn from user interactions and store insights in memory.
        
        Args:
            interaction_type: Type of interaction (query, definition_request, validation, etc.)
            data: Interaction data to learn from
            
        Returns:
            Success status
        """
        if not self.use_memory or not self.memory:
            return False
        
        try:
            # Create learning memory based on interaction type
            if interaction_type == "query":
                text = f"User queried: {data.get('query', '')}. Response provided: {data.get('response', '')}"
            elif interaction_type == "definition_request":
                text = f"Product definition requested: {data.get('product_code', '')}. Factors: {data.get('factors', [])}"
            elif interaction_type == "validation":
                text = f"Validation performed for: {data.get('product_code', '')}. Status: {data.get('valid', False)}"
            elif interaction_type == "usage_pattern":
                text = f"Usage pattern detected: {data.get('pattern', '')}. Frequency: {data.get('frequency', 1)}"
            else:
                text = f"Interaction: {interaction_type}. Data: {str(data)[:200]}"
            
            result = self.memory.add_memory(
                text=text,
                user_id=self.user_id,
                agent_id=self.agent_id,
                run_id=f"learning_{datetime.now().strftime('%Y%m%d')}",
                metadata={
                    "category": f"learning_{interaction_type}",
                    "type": "learning",
                    "priority": "low",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            logger.info(f"Learned from {interaction_type} interaction")
            return True
            
        except Exception as e:
            logger.error(f"Error learning from interaction: {e}")
            return False
    
    def search_risk_factors(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for risk factors in memory based on a query.
        
        Args:
            query: Search query (e.g., "driver age factors", "discount factors")
            category: Optional category filter
            
        Returns:
            List of matching risk factors
        """
        if not self.use_memory or not self.memory:
            logger.warning("Memory not enabled, cannot search risk factors")
            return []
        
        try:
            # Enhance query with category if provided
            search_query = query
            if category:
                search_query = f"{query} in {category} category"
            
            results = self.query_knowledge(search_query, limit=10)
            
            # Filter for risk factor related knowledge
            risk_factor_results = [
                r for r in results 
                if 'risk_factor' in r.get('metadata', {}).get('category', '').lower()
                or 'risk factor' in r['text'].lower()
            ]
            
            logger.info(f"Found {len(risk_factor_results)} risk factors matching: '{query}'")
            return risk_factor_results
            
        except Exception as e:
            logger.error(f"Error searching risk factors: {e}")
            return []
    
    def get_product_knowledge(self, product_code: str) -> Dict[str, Any]:
        """
        Get comprehensive knowledge about a product from memory.
        
        Args:
            product_code: Product code to query
            
        Returns:
            Dictionary with product knowledge and definition
        """
        # Start with hardcoded definition
        product = self.get_product_definition(product_code)
        
        result = {
            "product_code": product_code,
            "definition": product,
            "memory_knowledge": []
        }
        
        if not self.use_memory or not self.memory:
            return result
        
        try:
            # Query memory for additional knowledge
            query = f"What do you know about {product_code} product?"
            knowledge = self.query_knowledge(query, limit=5)
            result["memory_knowledge"] = knowledge
            
            # Record this query as a learning opportunity
            self.learn_from_interaction("definition_request", {
                "product_code": product_code,
                "factors": len(product.risk_factors) if product else 0
            })
            
            logger.info(f"Retrieved product knowledge for: {product_code}")
            
        except Exception as e:
            logger.error(f"Error getting product knowledge: {e}")
        
        return result
    
    def answer_question(self, question: str) -> str:
        """
        Answer questions using memory-based knowledge.
        
        Args:
            question: Natural language question about products or risk factors
            
        Returns:
            Answer from memory and loaded product definitions
        """
        logger.info(f"Answering question: '{question}'")
        
        # Try to answer using memory first
        memory_results = []
        if self.use_memory and self.memory:
            try:
                memory_results = self.query_knowledge(question, limit=5)
            except Exception as e:
                logger.error(f"Error querying memory: {e}")
        
        # Build answer
        answer_parts = []
        
        # Add memory-based knowledge with better formatting
        if memory_results:
            answer_parts.append("## 📚 Knowledge from Memory\n")
            for idx, result in enumerate(memory_results, 1):
                text = result['text']
                score = result.get('score', 0)
                metadata = result.get('metadata', {})
                
                # Format each result nicely
                answer_parts.append(f"### {idx}. Relevance Score: {score:.3f}")
                answer_parts.append(f"{text}\n")
                
                # Add metadata if useful
                if metadata:
                    category = metadata.get('category', '')
                    if category:
                        answer_parts.append(f"*Category: {category}*\n")
        
        # Query mem0 for product-specific information if relevant
        question_lower = question.lower()
        product_found = False
        
        # Check for product-specific questions by querying mem0
        available_products = self.list_available_products()
        
        for prod_code in available_products:
            if prod_code.lower() in question_lower:
                product_found = True
                prod = self.get_product_definition(prod_code)
                
                if prod:
                    answer_parts.append(f"\n## 📦 Product Definition (from mem0): {prod.product_name}\n")
                    answer_parts.append(f"**Product Code:** {prod.product_code}\n")
                    answer_parts.append(f"**Total Risk Factors:** {len(prod.risk_factors)}\n")
                    
                    answer_parts.append("\n### 🎯 Risk Factors:\n")
                    for rf in prod.risk_factors:
                        answer_parts.append(f"**{rf.risk_factor_name}**")
                        answer_parts.append(f"  - Subject: {rf.risk_subject}")
                        answer_parts.append(f"  - Description: {rf.description}")
                        answer_parts.append(f"  - Weight: {rf.weight}")
                        answer_parts.append(f"  - Required: {'Yes' if rf.required else 'No'}\n")
                    
                    # Add coverage options
                    if prod.coverage_options:
                        answer_parts.append("\n### 🛡️ Coverage Options:\n")
                        for cov_type, cov_details in prod.coverage_options.items():
                            answer_parts.append(f"**{cov_type.replace('_', ' ').title()}:** {cov_details}\n")
        
        # Check for general risk factor questions
        if not product_found and ('risk factor' in question_lower or 'factor' in question_lower):
            # Query mem0 for all risk factors
            all_risk_factors = set()
            for prod_code in available_products:
                prod = self.get_product_definition(prod_code)
                if prod:
                    for rf in prod.risk_factors:
                        all_risk_factors.add((rf.risk_subject, rf.risk_factor_name, rf.description))
            
            if all_risk_factors:
                answer_parts.append("\n## 🎯 Available Risk Factors (from mem0):\n")
                for subject, name, desc in sorted(all_risk_factors):
                    answer_parts.append(f"**{name}** ({subject})")
                    answer_parts.append(f"  {desc}\n")
        
        # Check for product list questions
        if 'product' in question_lower and ('list' in question_lower or 'available' in question_lower or 'what' in question_lower):
            if not product_found:
                if available_products:
                    answer_parts.append("\n## 📦 Available Products (from mem0):\n")
                    for prod_code in available_products:
                        prod = self.get_product_definition(prod_code)
                        if prod:
                            answer_parts.append(f"**{prod.product_name}** (`{prod_code}`)")
                            answer_parts.append(f"  - {len(prod.risk_factors)} risk factors")
                            answer_parts.append(f"  - {len(prod.coverage_options)} coverage options\n")
                else:
                    answer_parts.append("\n## ⚠️ No Products Available\n")
                    answer_parts.append("No product definitions found in mem0. Use `store_product_to_memory()` to add products.\n")
        
        if not answer_parts:
            if not available_products:
                answer_parts.append("## ⚠️ No Knowledge Available\n")
                answer_parts.append("The agent's mem0 is empty. Please load or store product definitions first.\n")
                answer_parts.append("\n**To get started:**")
                answer_parts.append("1. Use `store_product_to_memory()` to add product definitions")
                answer_parts.append("2. Use `load_product_from_rules_dir()` to import from rule files")
                answer_parts.append("3. Run the bootstrap script: `python bootstrap_product_memory.py --sample-data`")
            else:
                answer_parts.append("## ℹ️ I can help you with:\n")
                answer_parts.append("**Available Products (from mem0):**")
                for prod_code in available_products:
                    answer_parts.append(f"  - {prod_code}")
                answer_parts.append("\n**Topics I know about:**")
                answer_parts.append("  - Risk factors and their definitions")
                answer_parts.append("  - Coverage options and limits")
                answer_parts.append("  - Product configurations")
                answer_parts.append("  - Assessment rules")
                answer_parts.append("\n**Example questions:**")
                answer_parts.append("  - Tell me about [product name]")
                answer_parts.append("  - What risk factors are available?")
                answer_parts.append("  - List all available products")
        
        answer = "\n".join(answer_parts)
        
        # Learn from this interaction
        if self.use_memory:
            self.learn_from_interaction("query", {
                "query": question,
                "response": answer[:200]
            })
        
        return answer
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the agent's memory.
        
        Returns:
            Dictionary with memory statistics
        """
        if not self.use_memory or not self.memory:
            return {"enabled": False, "message": "Memory not enabled"}
        
        try:
            memories = self.memory.get_memories(
                user_id=self.user_id,
                agent_id=self.agent_id
            )
            
            return {
                "enabled": True,
                "total_memories": len(memories),
                "agent_id": self.agent_id,
                "user_id": self.user_id
            }
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {"enabled": True, "error": str(e)}
