"""
Product Definition Agent - Pure Memory-Driven Agent

A lightweight, stateless agent that stores and retrieves product definitions
from mem0 vector database. No hardcoded knowledge, no prompt engineering.

Core Responsibilities:
1. Store product definitions in mem0
2. Retrieve product definitions from mem0
3. Search for risk factors using semantic search
4. Track interactions for learning

Architecture:
- Zero hardcoded knowledge
- Pure memory operations
- Stateless design
- Semantic search-based retrieval
"""

import logging
import json
from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from src.memory.memory_layer import MemoryLayer

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
    Pure memory-driven agent - all operations are memory reads/writes.
    No hardcoded knowledge, no complex logic, just memory operations.
    """
    
    def __init__(
        self,
        agent_id: str = "product_definition_agent",
        user_id: str = "system"
    ):
        """
        Initialize the memory-driven agent.
        
        Args:
            agent_id: Unique identifier for this agent
            user_id: User/system identifier for memory isolation
        """
        self.agent_id = agent_id
        self.user_id = user_id
        
        # Initialize memory layer
        try:
            self.memory = MemoryLayer(
                llm_provider="openai",
                temperature=0.3,
                max_tokens=4000
            )
            logger.info(f"✅ Memory layer initialized for agent: {agent_id}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize memory layer: {e}")
            raise RuntimeError("ProductDefinitionAgent requires memory layer") from e
        
        logger.info("🚀 ProductDefinitionAgent ready - pure memory-driven mode")
            
    def _parse_product_from_memory(self, memory_result: Dict[str, Any]) -> Optional[ProductDefinition]:
        """Parse product definition from memory result."""
        try:
            # Extract text content
            text = memory_result.get('memory', memory_result.get('text', ''))
            metadata = memory_result.get('metadata', {})
            
            # Try JSON extraction
            if '{' in text and '}' in text:
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                json_str = text[start_idx:end_idx]
                data = json.loads(json_str)
                
                # Build product from parsed data
                product_code = data.get('product_code', data.get('productCode'))
                if not product_code:
                    return None
                
                # Parse risk factors
                risk_factors = []
                for rf_data in data.get('risk_factors', data.get('riskFactors', [])):
                    risk_factors.append(RiskFactorDefinition(
                        risk_subject=rf_data.get('risk_subject', rf_data.get('riskSubject', 'unknown')),
                        risk_factor_name=rf_data.get('risk_factor_name', rf_data.get('riskFactorName', '')),
                        description=rf_data.get('description', ''),
                        evaluation_rules=rf_data.get('evaluation_rules', rf_data.get('evaluationRules', [])),
                        required=rf_data.get('required', True),
                        weight=rf_data.get('weight', 1.0)
                    ))
                
                return ProductDefinition(
                    product_code=product_code,
                    product_name=data.get('product_name', data.get('productName', product_code)),
                    risk_factors=risk_factors,
                    assessment_rules=data.get('assessment_rules', data.get('assessmentRules', {})),
                    coverage_options=data.get('coverage_options', data.get('coverageOptions', {}))
                )
            
            return None
            
        except Exception as e:
            logger.debug(f"Failed to parse product from memory: {e}")
            return None
        
    def store_product(self, product: ProductDefinition) -> bool:
        """Store product definition to memory."""
        try:
            # Convert to dictionary
            product_dict = {
                "product_code": product.product_code,
                "product_name": product.product_name,
                "risk_factors": [asdict(rf) for rf in product.risk_factors],
                "assessment_rules": product.assessment_rules,
                "coverage_options": product.coverage_options
            }
            
            # Store as JSON
            text = f"Product: {product.product_name}\n{json.dumps(product_dict, indent=2)}"
            
            self.memory.add_memory(
                text=text,
                user_id=self.user_id,
                agent_id=self.agent_id,
                metadata={
                    "category": "product_definition",
                    "product_code": product.product_code,
                    "type": "definition"
                }
            )
            
            logger.info(f"💾 Stored product: {product.product_code}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store product: {e}")
            return False
    
    def get_product(self, product_code: str) -> Optional[ProductDefinition]:
        """Get product definition from memory."""
        try:
            query = f"product definition {product_code}"
            results = self.memory.search_memories(
                query=query,
                user_id=self.user_id,
                agent_id=self.agent_id,
                limit=5
            )
            
            # Find matching product
            for result in results:
                product = self._parse_product_from_memory(result)
                if product and product.product_code == product_code:
                    logger.info(f"📦 Retrieved product: {product_code}")
                    return product
            
            logger.warning(f"⚠️ Product not found: {product_code}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get product: {e}")
            return None
        
    def get_risk_factors(self, product_code: str) -> List[Tuple[str, str]]:
        """Get risk factor definitions as (risk_subject, risk_factor_name) tuples."""
        product = self.get_product(product_code)
        if not product:
            return []
        return [(rf.risk_subject, rf.risk_factor_name) for rf in product.risk_factors]
        
    def get_assessment_rules(self, product_code: str, risk_factor_name: Optional[str] = None) -> Dict[str, Any]:
        """Get assessment rules for a product."""
        product = self.get_product(product_code)
        if not product:
            return {}
        
        if risk_factor_name:
            # Filter for specific risk factor
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
        """Get coverage options for a product."""
        product = self.get_product(product_code)
        return product.coverage_options if product else {}
        
    def list_products(self) -> List[str]:
        """List all available product codes from memory."""
        try:
            query = "all product definitions"
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
            
            logger.info(f"📋 Found {len(product_codes)} products")
            return sorted(list(product_codes))
            
        except Exception as e:
            logger.error(f"❌ Failed to list products: {e}")
            return []
        
    def validate_product(self, product_code: str) -> Dict[str, Any]:
        """Validate product configuration."""
        result = {
            "product_code": product_code,
            "valid": False,
            "issues": [],
            "warnings": []
        }
        
        product = self.get_product(product_code)
        if not product:
            result["issues"].append(f"Product not found: {product_code}")
            return result
            
        # Check risk factors
        if not product.risk_factors:
            result["issues"].append("No risk factors defined")
            
        # Check required risk factors have rules
        for rf in product.risk_factors:
            if rf.required and not rf.evaluation_rules:
                result["issues"].append(f"Required factor '{rf.risk_factor_name}' has no rules")
                
        # Check rule references
        for rf in product.risk_factors:
            for rule_id in rf.evaluation_rules:
                if rule_id not in product.assessment_rules:
                    result["warnings"].append(f"Rule '{rule_id}' not found")
                    
        result["valid"] = len(result["issues"]) == 0
        logger.info(f"✅ Validated {product_code}: {result['valid']}")
        return result
    
    # ==================== Memory Search Methods ====================
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search memory using semantic search."""
        try:
            results = self.memory.search_memories(
                query=query,
                user_id=self.user_id,
                agent_id=self.agent_id,
                limit=limit
            )
            
            # Normalize results
            normalized = []
            for result in results:
                if isinstance(result, dict):
                    normalized.append({
                        "text": result.get('memory', result.get('text', str(result))),
                        "score": result.get('score', 0.0),
                        "metadata": result.get('metadata', {})
                    })
            
            logger.info(f"🔍 Found {len(normalized)} results for: '{query}'")
            return normalized
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def search_risk_factors(self, query: str) -> List[Dict[str, Any]]:
        """Search for risk factors in memory."""
        try:
            results = self.search(f"risk factor {query}", limit=10)
            
            # Filter for risk factor content
            risk_factors = [
                r for r in results 
                if 'risk' in r['text'].lower() or 'factor' in r['text'].lower()
            ]
            
            logger.info(f"🎯 Found {len(risk_factors)} risk factors")
            return risk_factors
            
        except Exception as e:
            logger.error(f"❌ Risk factor search failed: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        try:
            memories = self.memory.get_memories(
                user_id=self.user_id,
                agent_id=self.agent_id
            )
            
            return {
                "agent_id": self.agent_id,
                "user_id": self.user_id,
                "total_memories": len(memories),
                "products": len(self.list_products())
            }
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {"error": str(e)}
