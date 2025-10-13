"""
Multi-Agent Graph Orchestration System

This module implements the Graph-based multi-agent system using Strands Agents
to orchestrate the insurance risk assessment and premium calculation workflow.

Based on the architecture design, this implements the PlantUML flow:
1. Orchestrator Agent receives and validates applications
2. Product Definition Agent provides risk factors and rules
3. Risk Factor Reasoning Agent determines risk tiers
4. Data Lookup Agent provides mapping values
5. Premium Calculation Agent calculates final premium
"""

import logging
from typing import Any, Dict, List, Optional, Union
import json
from dataclasses import dataclass, asdict

# Strands Agents imports
try:
    from strands import Agent
    from strands.multiagent import GraphBuilder
    from strands.types.content import ContentBlock
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False
    logging.warning("Strands Agents not available - falling back to mock implementation")

# Local imports
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.product_definition_agent import ProductDefinitionAgent
from src.agents.data_lookup_agent import DataLookupAgent
from src.agents.premium_calculation_agent import PremiumCalculationAgent
from src.agents.risk_factor_agent import assess as risk_factor_assess
from src.models.risk_profile import RiskProfile
from src.models.assessment_result import AssessmentResult
from src.gateway.agent_factory import init_agent

logger = logging.getLogger(__name__)


@dataclass
class MultiAgentResult:
    """Result from multi-agent graph execution."""
    status: str
    session_id: str
    risk_profile: Dict[str, Any]
    product_definition: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    premium_calculation: Dict[str, Any]
    execution_order: List[str]
    execution_time_ms: int
    errors: List[str]
    warnings: List[str]


class InsuranceRatingEngine:
    """
    Multi-Agent Graph implementation for insurance rating engine.
    
    This class orchestrates the complete workflow from application input
    to final premium calculation using a directed graph of specialized agents.
    """
    
    def __init__(self, product_code: str = "Monthly-Comfort"):
        """
        Initialize the insurance rating engine.
        
        Args:
            product_code: Default product code for processing
        """
        self.product_code = product_code
        self.orchestrator = OrchestratorAgent()
        self.product_agent = ProductDefinitionAgent()
        self.lookup_agent = DataLookupAgent()
        self.premium_agent = PremiumCalculationAgent()
        
        # Initialize Strands agents if available
        self.strands_agents = {}
        if STRANDS_AVAILABLE:
            self._initialize_strands_agents()
            
        self.graph = None
        self.execution_history: List[MultiAgentResult] = []
        
    def _initialize_strands_agents(self) -> None:
        """Initialize Strands Agent instances for each role using OpenAI model configuration."""
        try:
            # Use the same model configuration as demo_agent.py via agent factory
            base_agent = init_agent()
            model = base_agent.model  # Get the model from the initialized agent
            
            # Product Definition Agent
            self.strands_agents["product_definition"] = Agent(
                model=model,
                name="product_definition_agent",
                system_prompt="""You are a Product Definition Agent for an insurance rating engine.
                
Your responsibilities:
1. Define required risk factors for insurance products
2. Provide risk factor definitions and assessment rules
3. Validate product configurations
4. Ensure all risk factors have proper evaluation rules

You work with product codes like Monthly-Economy, Monthly-Comfort, and Monthly-Turbo.
Always provide structured responses with risk factor definitions and assessment rules."""
            )
            
            # Risk Factor Reasoning Agent (enhanced version of existing)
            self.strands_agents["risk_reasoning"] = Agent(
                model=model,
                name="risk_reasoning_agent", 
                system_prompt="""You are a Risk Factor Reasoning Agent for insurance risk assessment.
                
Your responsibilities:
1. Apply assessment rules to application data
2. Determine risk tier values (LOW, MEDIUM, HIGH, VERY_HIGH)
3. Validate rule application results
4. Provide detailed reasoning for risk assessments

You analyze driver records, vehicle information, and policy details to determine risk factors.
Always provide clear reasoning and evidence for your risk tier determinations."""
            )
            
            # Data Lookup Agent
            self.strands_agents["data_lookup"] = Agent(
                model=model,
                name="data_lookup_agent",
                system_prompt="""You are a Data Lookup Agent for insurance calculations.
                
Your responsibilities:
1. Provide mapping values during risk calculation
2. Map risk tiers to specific multiplier values
3. Provide coverage values for premium calculation
4. Maintain consistency in lookup mappings

You have access to lookup tables for risk multipliers, discounts, and coverage values.
Always ensure your mappings are consistent and properly validated."""
            )
            
            # Premium Calculation Agent
            self.strands_agents["premium_calculation"] = Agent(
                model=model,
                name="premium_calculation_agent",
                system_prompt="""You are a Premium Calculation Agent for insurance pricing.
                
Your responsibilities:
1. Apply premium calculation formulas
2. Process risk factors and coverage values
3. Calculate final premium amounts with proper validation
4. Provide detailed calculation breakdowns

You must ensure all calculations are accurate and properly documented with clear breakdowns."""
            )
            
            logger.info("Strands agents initialized successfully with OpenAI model configuration")
            
        except Exception as e:
            logger.error(f"Failed to initialize Strands agents: {e}")
            self.strands_agents = {}
            
    def build_graph(self) -> Optional[Any]:
        """
        Build the multi-agent graph using Strands GraphBuilder.
        
        Returns:
            Strands Graph instance if successful, None otherwise
        """
        if not STRANDS_AVAILABLE or not self.strands_agents:
            logger.warning("Strands not available - cannot build graph")
            return None
            
        try:
            from strands.multiagent import GraphBuilder
            
            builder = GraphBuilder()
            
            # Add nodes (agents)
            builder.add_node(self.strands_agents["product_definition"], "product_definition")
            builder.add_node(self.strands_agents["risk_reasoning"], "risk_reasoning")
            builder.add_node(self.strands_agents["data_lookup"], "data_lookup")
            builder.add_node(self.strands_agents["premium_calculation"], "premium_calculation")
            
            # Add edges (dependencies) following the architecture flow
            builder.add_edge("product_definition", "risk_reasoning")
            builder.add_edge("risk_reasoning", "data_lookup")
            builder.add_edge("data_lookup", "premium_calculation")
            
            # Set entry point
            builder.set_entry_point("product_definition")
            
            # Configure execution limits
            builder.set_execution_timeout(300)  # 5 minutes
            builder.set_max_node_executions(10)  # Prevent infinite loops
            
            # Build the graph
            self.graph = builder.build()
            
            logger.info("Multi-agent graph built successfully")
            return self.graph
            
        except Exception as e:
            logger.error(f"Failed to build graph: {e}")
            return None
            
    def process_application_with_graph(
        self, 
        raw_application: str, 
        product_code: Optional[str] = None
    ) -> MultiAgentResult:
        """
        Process insurance application using the multi-agent graph.
        
        Args:
            raw_application: Raw JSON application data
            product_code: Optional product code override
            
        Returns:
            MultiAgentResult with complete processing results
        """
        import time
        start_time = time.time()
        
        product_code = product_code or self.product_code
        session_id = f"graph_session_{int(start_time)}"
        
        result = MultiAgentResult(
            status="processing",
            session_id=session_id,
            risk_profile={},
            product_definition={},
            risk_assessment={},
            premium_calculation={},
            execution_order=[],
            execution_time_ms=0,
            errors=[],
            warnings=[]
        )
        
        try:
            # Initialize context with orchestrator
            context = self.orchestrator.initialize_context(product_code)
            profile = self.orchestrator.validate_application(raw_application)
            result.risk_profile = dict(profile)
            
            if STRANDS_AVAILABLE and self.graph:
                # Use Strands Graph for processing
                result = self._process_with_strands_graph(result, profile, product_code, context)
            else:
                # Fallback to sequential processing
                result = self._process_sequential(result, profile, product_code, context)
                
        except Exception as e:
            logger.error(f"Graph processing failed: {e}")
            result.status = "failed"
            result.errors.append(str(e))
            
        # Calculate execution time
        result.execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Store in history
        self.execution_history.append(result)
        
        return result
        
    def _process_with_strands_graph(
        self, 
        result: MultiAgentResult, 
        profile: RiskProfile, 
        product_code: str,
        context: Dict[str, Any]
    ) -> MultiAgentResult:
        """Process using Strands Graph orchestration."""
        try:
            # Prepare input for the graph
            graph_input = {
                "task": f"Process insurance application for product {product_code}",
                "application_data": dict(profile),
                "product_code": product_code,
                "context": context
            }
            
            # Execute the graph
            graph_result = self.graph(json.dumps(graph_input, indent=2))
            
            # Process graph results
            if hasattr(graph_result, 'results') and graph_result.results:
                result.execution_order = [node.node_id for node in graph_result.execution_order]
                
                # Extract results from each node
                for node_id, node_result in graph_result.results.items():
                    if node_id == "product_definition":
                        result.product_definition = self._extract_product_definition_result(node_result)
                    elif node_id == "risk_reasoning":
                        result.risk_assessment = self._extract_risk_assessment_result(node_result)
                    elif node_id == "premium_calculation":
                        result.premium_calculation = self._extract_premium_result(node_result)
                        
                result.status = "completed" if graph_result.status.name == "COMPLETED" else "failed"
            else:
                result.status = "failed"
                result.errors.append("No results from graph execution")
                
        except Exception as e:
            logger.error(f"Strands graph processing failed: {e}")
            result.status = "failed"
            result.errors.append(f"Graph execution error: {e}")
            
        return result
        
    def _process_sequential(
        self, 
        result: MultiAgentResult, 
        profile: RiskProfile, 
        product_code: str,
        context: Dict[str, Any]
    ) -> MultiAgentResult:
        """Fallback sequential processing without Strands Graph."""
        try:
            # Step 1: Product Definition
            product_def = self.product_agent.get_product_definition(product_code)
            if product_def:
                result.product_definition = asdict(product_def)
                result.execution_order.append("product_definition")
            else:
                result.warnings.append(f"Product definition not found for {product_code}")
                
            # Step 2: Risk Assessment using existing risk factor agent
            risk_assessment = risk_factor_assess(profile, product_code)
            result.risk_assessment = dict(risk_assessment)
            result.execution_order.append("risk_reasoning")
            
            # Step 3: Data Lookup for premium calculation
            base_premium = self.lookup_agent.lookup_base_premium(product_code)
            coverage_values = self.lookup_agent.lookup_coverage_values(product_code)
            result.execution_order.append("data_lookup")
            
            # Step 4: Premium Calculation
            premium_result = self.premium_agent.calculate_premium(
                base_premium=base_premium,
                risk_factors=result.risk_assessment,
                coverage_values=coverage_values,
                product_code=product_code
            )
            result.premium_calculation = asdict(premium_result)
            result.execution_order.append("premium_calculation")
            
            result.status = "completed"
            
        except Exception as e:
            logger.error(f"Sequential processing failed: {e}")
            result.status = "failed"
            result.errors.append(f"Sequential processing error: {e}")
            
        return result
        
    def _extract_product_definition_result(self, node_result: Any) -> Dict[str, Any]:
        """Extract product definition results from graph node."""
        # This would parse the LLM response and extract structured data
        # For now, return a placeholder
        return {
            "product_code": self.product_code,
            "risk_factors_defined": True,
            "rules_loaded": True
        }
        
    def _extract_risk_assessment_result(self, node_result: Any) -> Dict[str, Any]:
        """Extract risk assessment results from graph node."""
        # This would parse the LLM response and extract structured data
        # For now, return a placeholder
        return {
            "overall_risk_tier": "MEDIUM",
            "risk_factors": {
                "three_year_claim_free_discount": {"tier": "LOW", "discount": 0.15}
            },
            "confidence": 0.85
        }
        
    def _extract_premium_result(self, node_result: Any) -> Dict[str, Any]:
        """Extract premium calculation results from graph node."""
        # This would parse the LLM response and extract structured data
        # For now, return a placeholder
        return {
            "base_premium": 180.0,
            "total_premium": 165.0,
            "calculation_valid": True
        }
        
    def get_execution_history(self, limit: Optional[int] = None) -> List[MultiAgentResult]:
        """Get execution history."""
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history.copy()
        
    def clear_execution_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
        logger.info("Execution history cleared")
        
    def get_graph_status(self) -> Dict[str, Any]:
        """Get current status of the graph system."""
        return {
            "strands_available": STRANDS_AVAILABLE,
            "graph_built": self.graph is not None,
            "agents_initialized": len(self.strands_agents),
            "execution_count": len(self.execution_history),
            "product_code": self.product_code
        }


# Convenience function for easy usage
def create_rating_engine(product_code: str = "Monthly-Comfort") -> InsuranceRatingEngine:
    """
    Create and initialize an insurance rating engine.
    
    Args:
        product_code: Default product code
        
    Returns:
        Initialized InsuranceRatingEngine
    """
    engine = InsuranceRatingEngine(product_code)
    
    # Build the graph if Strands is available
    if STRANDS_AVAILABLE:
        engine.build_graph()
        
    return engine
