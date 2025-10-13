"""
Orchestrator Agent (Master Agent) - Multi-Agent System

This agent coordinates the overall workflow for insurance application processing:
1. Receives and validates insurance applications
2. Manages overall workflow coordination
3. Initializes context (timestamp, product type)
4. Coordinates risk factor processing loop
5. Collects and aggregates risk factor values
6. Manages the premium calculation process
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.models.risk_profile import RiskProfile
from src.models.assessment_result import AssessmentResult
from src.utils.data_parser import parse_application
from src.gateway.agent_factory import init_agent

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    Master Agent responsible for coordinating the entire insurance application workflow.
    """
    
    def __init__(self):
        """Initialize the orchestrator agent with necessary components."""
        self.agent = init_agent()
        self.context: Dict[str, Any] = {}
        
    def initialize_context(self, product_type: str = "Monthly-Comfort") -> Dict[str, Any]:
        """
        Initialize processing context with timestamp and product type.
        
        Args:
            product_type: The insurance product package type
            
        Returns:
            Initialized context dictionary
        """
        self.context = {
            "timestamp": datetime.now().isoformat(),
            "product_type": product_type,
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "risk_factors": {},
            "processing_status": "initialized"
        }
        
        logger.info(f"Context initialized: {self.context['session_id']}")
        return self.context
        
    def validate_application(self, raw_application: str) -> RiskProfile:
        """
        Validate and parse the insurance application.
        
        Args:
            raw_application: Raw JSON string of the insurance application
            
        Returns:
            Parsed and validated RiskProfile
            
        Raises:
            ValueError: If application validation fails
        """
        try:
            profile = parse_application(raw_application)
            
            # Log validation issues if any
            if profile.get("issues"):
                logger.warning(f"Application validation issues: {profile['issues']}")
                
            self.context["processing_status"] = "validated"
            logger.info("Application validated successfully")
            return profile
            
        except Exception as e:
            logger.error(f"Application validation failed: {e}")
            raise ValueError(f"Application validation failed: {e}") from e
            
    def process_application(
        self, 
        raw_application: str, 
        product_type: str = "Monthly-Comfort"
    ) -> Dict[str, Any]:
        """
        Main orchestration method that processes the entire application workflow.
        
        Args:
            raw_application: Raw JSON string of the insurance application
            product_type: The insurance product package type
            
        Returns:
            Complete processing result with all agent outputs
        """
        try:
            # Initialize context
            context = self.initialize_context(product_type)
            
            # Validate application
            profile = self.validate_application(raw_application)
            
            # Store profile in context
            context["risk_profile"] = profile
            context["processing_status"] = "processing"
            
            # This will be extended when we implement the Graph orchestration
            # For now, return the context with validated profile
            result = {
                "context": context,
                "profile": profile,
                "status": "ready_for_graph_processing",
                "message": "Application validated and ready for multi-agent graph processing"
            }
            
            logger.info(f"Application processed successfully: {context['session_id']}")
            return result
            
        except Exception as e:
            logger.error(f"Application processing failed: {e}")
            self.context["processing_status"] = "failed"
            self.context["error"] = str(e)
            raise
            
    def get_context(self) -> Dict[str, Any]:
        """Get the current processing context."""
        return self.context.copy()
        
    def update_context(self, updates: Dict[str, Any]) -> None:
        """Update the processing context with new information."""
        self.context.update(updates)
        logger.debug(f"Context updated: {list(updates.keys())}")
