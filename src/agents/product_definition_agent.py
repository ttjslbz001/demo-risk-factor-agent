"""
Product Definition Agent - Memory-Based Multi-Agent System

This agent is responsible for:
1. Defining required risk factors for products
2. Providing risk factor definitions <risk_subject, risk_factor_name>[]
3. Supplying assessment rules for each risk factor
4. Maintaining product-specific rule configurations
5. Defining how risk factors should be evaluated

Memory Features:
- Persistent knowledge about risk factors and products
- Learning from interactions and usage patterns
- Context-aware responses using semantic search
- Growing knowledge base over time
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
    Memory-based agent responsible for defining products, risk factors, and assessment rules.
    
    This agent uses persistent memory to:
    - Store and retrieve risk factor knowledge
    - Learn from interactions
    - Provide context-aware responses
    - Grow its knowledge base over time
    """
    
    def __init__(
        self, 
        rules_dir: str = "docs/insurance_risk_factor_agent/3_year_claim_free_discount",
        use_memory: bool = True,
        agent_id: str = "product_definition_agent",
        user_id: str = "system"
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
        self.product_definitions: Dict[str, ProductDefinition] = {}
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
        
        self._load_product_definitions()
        
    def _load_product_definitions(self) -> None:
        """Load product definitions and rules."""
        try:
            # Load rules from the rules directory
            rules = load_rules(self.rules_dir)
            
            # Define the Monthly-Comfort product (demo product)
            comfort_product = ProductDefinition(
                product_code="Monthly-Comfort",
                product_name="Monthly Comfort Package",
                risk_factors=[
                    RiskFactorDefinition(
                        risk_subject="driver",
                        risk_factor_name="three_year_claim_free_discount",
                        description="Three-year claim-free driving discount assessment",
                        evaluation_rules=[rule["id"] for rule in rules],
                        required=True,
                        weight=1.0
                    ),
                    RiskFactorDefinition(
                        risk_subject="driver",
                        risk_factor_name="driving_record_classification",
                        description="Driver record classification based on violations and claims",
                        evaluation_rules=["D04_Driving_Record_Classification"],
                        required=True,
                        weight=1.2
                    ),
                    RiskFactorDefinition(
                        risk_subject="driver",
                        risk_factor_name="driver_classification",
                        description="Basic driver classification by age and experience",
                        evaluation_rules=["D03_Driver_Classification"],
                        required=True,
                        weight=0.8
                    )
                ],
                assessment_rules={rule["id"]: rule for rule in rules},
                coverage_options={
                    "liability_coverage": {"min": 25000, "max": 100000, "default": 50000},
                    "comprehensive": {"available": True, "deductible_options": [250, 500, 1000]},
                    "collision": {"available": True, "deductible_options": [250, 500, 1000]}
                }
            )
            
            self.product_definitions["Monthly-Comfort"] = comfort_product
            
            # Add other product definitions (placeholders for future expansion)
            self._add_economy_product()
            self._add_turbo_product()
            
            logger.info(f"Loaded {len(self.product_definitions)} product definitions")
            
        except Exception as e:
            logger.error(f"Failed to load product definitions: {e}")
            raise RuntimeError(f"ProductDefinitionLoadError: {e}") from e
            
    def _add_economy_product(self) -> None:
        """Add Monthly-Economy product definition (placeholder)."""
        economy_product = ProductDefinition(
            product_code="Monthly-Economy",
            product_name="Monthly Economy Package",
            risk_factors=[
                RiskFactorDefinition(
                    risk_subject="driver",
                    risk_factor_name="basic_driver_assessment",
                    description="Basic driver assessment for economy package",
                    evaluation_rules=["basic_rules"],
                    required=True,
                    weight=1.0
                )
            ],
            assessment_rules={},
            coverage_options={
                "liability_coverage": {"min": 15000, "max": 50000, "default": 25000}
            }
        )
        self.product_definitions["Monthly-Economy"] = economy_product
        
    def _add_turbo_product(self) -> None:
        """Add Monthly-Turbo product definition (placeholder)."""
        turbo_product = ProductDefinition(
            product_code="Monthly-Turbo",
            product_name="Monthly Turbo Package",
            risk_factors=[
                RiskFactorDefinition(
                    risk_subject="driver",
                    risk_factor_name="comprehensive_risk_assessment",
                    description="Comprehensive risk assessment for turbo package",
                    evaluation_rules=["comprehensive_rules"],
                    required=True,
                    weight=1.5
                )
            ],
            assessment_rules={},
            coverage_options={
                "liability_coverage": {"min": 50000, "max": 250000, "default": 100000},
                "comprehensive": {"available": True, "deductible_options": [100, 250, 500]},
                "collision": {"available": True, "deductible_options": [100, 250, 500]},
                "rental_car": {"available": True, "daily_limit": 50}
            }
        )
        self.product_definitions["Monthly-Turbo"] = turbo_product
        
    def get_product_definition(self, product_code: str) -> Optional[ProductDefinition]:
        """
        Get the complete product definition for a given product code.
        
        Args:
            product_code: The product code (e.g., "Monthly-Comfort")
            
        Returns:
            ProductDefinition if found, None otherwise
        """
        return self.product_definitions.get(product_code)
        
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
        Get list of available product codes.
        
        Returns:
            List of available product codes
        """
        return list(self.product_definitions.keys())
        
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
        Answer questions using both hardcoded definitions and memory knowledge.
        
        Args:
            question: Natural language question about products or risk factors
            
        Returns:
            Answer combining definitions and memory
        """
        logger.info(f"Answering question: '{question}'")
        
        # Try to answer using memory first
        memory_results = []
        if self.use_memory and self.memory:
            try:
                memory_results = self.query_knowledge(question, limit=3)
            except Exception as e:
                logger.error(f"Error querying memory: {e}")
        
        # Build answer
        answer_parts = []
        
        # Add memory-based knowledge
        if memory_results:
            answer_parts.append("Based on my knowledge:")
            for idx, result in enumerate(memory_results[:3], 1):
                text = result['text']
                # Clean up the text
                if len(text) > 200:
                    text = text[:200] + "..."
                answer_parts.append(f"{idx}. {text}")
        
        # Add hardcoded product definitions if relevant
        question_lower = question.lower()
        if any(prod.lower() in question_lower for prod in self.product_definitions.keys()):
            for prod_code in self.product_definitions.keys():
                if prod_code.lower() in question_lower:
                    prod = self.product_definitions[prod_code]
                    answer_parts.append(f"\nProduct: {prod.product_name} ({prod.product_code})")
                    answer_parts.append(f"Risk Factors: {len(prod.risk_factors)}")
                    for rf in prod.risk_factors:
                        answer_parts.append(f"  - {rf.risk_factor_name} (weight: {rf.weight})")
        
        if not answer_parts:
            answer_parts.append("I don't have specific information about that. Please try rephrasing your question or ask about:")
            answer_parts.append("- Available products (Monthly-Comfort, Monthly-Economy, Monthly-Turbo)")
            answer_parts.append("- Risk factors and their categories")
            answer_parts.append("- Coverage options and limits")
        
        answer = "\n".join(answer_parts)
        
        # Learn from this interaction
        if self.use_memory:
            self.learn_from_interaction("query", {
                "query": question,
                "response": answer[:100]
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
