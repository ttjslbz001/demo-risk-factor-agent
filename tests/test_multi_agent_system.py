"""
Integration tests for the multi-agent system.

Tests the complete multi-agent graph orchestration system including:
- Orchestrator Agent
- Product Definition Agent  
- Data Lookup Agent
- Premium Calculation Agent
- Graph-based workflow coordination
"""

import json
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.product_definition_agent import ProductDefinitionAgent
from src.agents.data_lookup_agent import DataLookupAgent
from src.agents.premium_calculation_agent import PremiumCalculationAgent
from src.agents.multi_agent_graph import InsuranceRatingEngine, create_rating_engine


class TestOrchestratorAgent:
    """Test the Orchestrator Agent functionality."""
    
    def test_initialize_context(self):
        """Test context initialization."""
        orchestrator = OrchestratorAgent()
        context = orchestrator.initialize_context("Monthly-Comfort")
        
        assert context["product_type"] == "Monthly-Comfort"
        assert "timestamp" in context
        assert "session_id" in context
        assert context["processing_status"] == "initialized"
        assert context["risk_factors"] == {}
        
    def test_validate_application_success(self):
        """Test successful application validation."""
        orchestrator = OrchestratorAgent()
        
        sample_application = json.dumps({
            "household": {"address": "123 Main St"},
            "drivers": [{"name": "John Doe", "age": 30}],
            "vehicles": [{"make": "Toyota", "model": "Camry", "year": 2020}]
        })
        
        with patch('src.agents.orchestrator_agent.parse_application') as mock_parse:
            mock_parse.return_value = {
                "household": {"address": "123 Main St"},
                "drivers": [{"name": "John Doe", "age": 30}],
                "vehicles": [{"make": "Toyota", "model": "Camry", "year": 2020}],
                "issues": []
            }
            
            profile = orchestrator.validate_application(sample_application)
            assert profile["household"]["address"] == "123 Main St"
            assert len(profile["drivers"]) == 1
            assert len(profile["vehicles"]) == 1
            
    def test_process_application_workflow(self):
        """Test the complete application processing workflow."""
        orchestrator = OrchestratorAgent()
        
        sample_application = json.dumps({
            "household": {"address": "123 Main St"},
            "drivers": [{"name": "John Doe", "age": 30}],
            "vehicles": [{"make": "Toyota", "model": "Camry", "year": 2020}]
        })
        
        with patch('src.agents.orchestrator_agent.parse_application') as mock_parse:
            mock_parse.return_value = {
                "household": {"address": "123 Main St"},
                "drivers": [{"name": "John Doe", "age": 30}],
                "vehicles": [{"make": "Toyota", "model": "Camry", "year": 2020}],
                "issues": []
            }
            
            result = orchestrator.process_application(sample_application)
            
            assert result["status"] == "ready_for_graph_processing"
            assert "context" in result
            assert "profile" in result
            assert result["context"]["processing_status"] == "processing"


class TestProductDefinitionAgent:
    """Test the Product Definition Agent functionality."""
    
    def test_initialization(self):
        """Test agent initialization."""
        with patch('src.agents.product_definition_agent.load_rules') as mock_load:
            mock_load.return_value = [
                {"id": "P36_Three_Year_Safe_Driving_Discount", "title": "Test Rule"}
            ]
            
            agent = ProductDefinitionAgent()
            assert "Monthly-Comfort" in agent.product_definitions
            assert "Monthly-Economy" in agent.product_definitions
            assert "Monthly-Turbo" in agent.product_definitions
            
    def test_get_product_definition(self):
        """Test getting product definition."""
        with patch('src.agents.product_definition_agent.load_rules') as mock_load:
            mock_load.return_value = [
                {"id": "P36_Three_Year_Safe_Driving_Discount", "title": "Test Rule"}
            ]
            
            agent = ProductDefinitionAgent()
            product = agent.get_product_definition("Monthly-Comfort")
            
            assert product is not None
            assert product.product_code == "Monthly-Comfort"
            assert product.product_name == "Monthly Comfort Package"
            assert len(product.risk_factors) > 0
            
    def test_get_risk_factor_definitions(self):
        """Test getting risk factor definitions."""
        with patch('src.agents.product_definition_agent.load_rules') as mock_load:
            mock_load.return_value = [
                {"id": "P36_Three_Year_Safe_Driving_Discount", "title": "Test Rule"}
            ]
            
            agent = ProductDefinitionAgent()
            risk_factors = agent.get_risk_factor_definitions("Monthly-Comfort")
            
            assert len(risk_factors) > 0
            assert all(len(rf) == 2 for rf in risk_factors)  # (subject, name) tuples
            
    def test_validate_product_configuration(self):
        """Test product configuration validation."""
        with patch('src.agents.product_definition_agent.load_rules') as mock_load:
            mock_load.return_value = [
                {"id": "P36_Three_Year_Safe_Driving_Discount", "title": "Test Rule"}
            ]
            
            agent = ProductDefinitionAgent()
            validation = agent.validate_product_configuration("Monthly-Comfort")
            
            assert validation["product_code"] == "Monthly-Comfort"
            assert "valid" in validation
            assert "issues" in validation
            assert "warnings" in validation


class TestDataLookupAgent:
    """Test the Data Lookup Agent functionality."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = DataLookupAgent()
        assert len(agent.lookup_tables) > 0
        assert "risk_tier_multipliers" in agent.lookup_tables
        assert "base_premiums" in agent.lookup_tables
        
    def test_lookup_risk_tier_multiplier(self):
        """Test risk tier multiplier lookup."""
        agent = DataLookupAgent()
        
        low_multiplier = agent.lookup_risk_tier_multiplier("LOW")
        medium_multiplier = agent.lookup_risk_tier_multiplier("MEDIUM")
        high_multiplier = agent.lookup_risk_tier_multiplier("HIGH")
        
        assert low_multiplier < medium_multiplier < high_multiplier
        assert low_multiplier == 0.8
        assert medium_multiplier == 1.0
        assert high_multiplier == 1.3
        
    def test_lookup_claim_free_discount(self):
        """Test claim-free discount lookup."""
        agent = DataLookupAgent()
        
        discount_0 = agent.lookup_claim_free_discount(0)
        discount_3 = agent.lookup_claim_free_discount(3)
        discount_5 = agent.lookup_claim_free_discount(5)
        
        assert discount_0["discount"] == 0.0
        assert discount_3["discount"] == 0.15
        assert discount_5["discount"] == 0.20
        assert discount_0["tier"] == "HIGH"
        assert discount_3["tier"] == "LOW"
        
    def test_lookup_coverage_values(self):
        """Test coverage values lookup."""
        agent = DataLookupAgent()
        
        comfort_coverage = agent.lookup_coverage_values("Monthly-Comfort")
        economy_coverage = agent.lookup_coverage_values("Monthly-Economy")
        
        assert "liability" in comfort_coverage
        assert "comprehensive" in comfort_coverage
        assert comfort_coverage["liability"]["base"] > economy_coverage["liability"]["base"]
        
    def test_validate_lookup_tables(self):
        """Test lookup table validation."""
        agent = DataLookupAgent()
        validation = agent.validate_lookup_tables()
        
        assert validation["valid"] is True
        assert validation["table_count"] > 0
        assert validation["total_entries"] > 0


class TestPremiumCalculationAgent:
    """Test the Premium Calculation Agent functionality."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = PremiumCalculationAgent()
        assert len(agent.calculation_history) == 0
        
    def test_calculate_premium_basic(self):
        """Test basic premium calculation."""
        agent = PremiumCalculationAgent()
        
        risk_factors = {
            "three_year_claim_free_discount": {"tier": "LOW", "discount": 0.15},
            "driving_record_classification": {"multiplier": 0.9, "tier": "LOW"},
            "driver_classification": {"base_rate": 1.0, "tier": "LOW"}
        }
        
        coverage_values = {
            "liability": {"base": 50000, "premium_factor": 1.0},
            "comprehensive": {"base": 30000, "premium_factor": 1.0}
        }
        
        result = agent.calculate_premium(
            base_premium=180.0,
            risk_factors=risk_factors,
            coverage_values=coverage_values,
            product_code="Monthly-Comfort"
        )
        
        assert result.base_premium == 180.0
        assert result.total_premium > 0
        assert result.validation_status == "valid"
        assert len(result.components) > 0
        assert len(result.discounts) > 0
        
    def test_calculation_with_high_risk(self):
        """Test premium calculation with high risk factors."""
        agent = PremiumCalculationAgent()
        
        risk_factors = {
            "three_year_claim_free_discount": {"tier": "HIGH", "discount": 0.0},
            "driving_record_classification": {"multiplier": 1.7, "tier": "VERY_HIGH"},
            "driver_classification": {"base_rate": 1.5, "tier": "HIGH"}
        }
        
        coverage_values = {
            "liability": {"base": 50000, "premium_factor": 1.0}
        }
        
        result = agent.calculate_premium(
            base_premium=180.0,
            risk_factors=risk_factors,
            coverage_values=coverage_values,
            product_code="Monthly-Comfort"
        )
        
        assert result.total_premium > result.base_premium
        assert result.risk_multiplier > 1.0
        
    def test_get_calculation_breakdown(self):
        """Test calculation breakdown generation."""
        agent = PremiumCalculationAgent()
        
        risk_factors = {"three_year_claim_free_discount": {"tier": "LOW", "discount": 0.15}}
        coverage_values = {"liability": {"base": 50000, "premium_factor": 1.0}}
        
        result = agent.calculate_premium(180.0, risk_factors, coverage_values, "Monthly-Comfort")
        breakdown = agent.get_calculation_breakdown(result)
        
        assert "summary" in breakdown
        assert "components" in breakdown
        assert "discounts" in breakdown
        assert "calculation_details" in breakdown


class TestInsuranceRatingEngine:
    """Test the complete Insurance Rating Engine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = create_rating_engine("Monthly-Comfort")
        
        assert engine.product_code == "Monthly-Comfort"
        assert engine.orchestrator is not None
        assert engine.product_agent is not None
        assert engine.lookup_agent is not None
        assert engine.premium_agent is not None
        
    def test_get_graph_status(self):
        """Test getting graph status."""
        engine = create_rating_engine()
        status = engine.get_graph_status()
        
        assert "strands_available" in status
        assert "graph_built" in status
        assert "agents_initialized" in status
        assert "execution_count" in status
        assert "product_code" in status
        
    @patch('src.agents.multi_agent_graph.STRANDS_AVAILABLE', False)
    def test_process_application_sequential_fallback(self):
        """Test processing application with sequential fallback."""
        engine = create_rating_engine("Monthly-Comfort")
        
        sample_application = json.dumps({
            "household": {"address": "123 Main St"},
            "drivers": [{"name": "John Doe", "age": 30, "license_years": 10}],
            "vehicles": [{"make": "Toyota", "model": "Camry", "year": 2020}]
        })
        
        with patch('src.agents.orchestrator_agent.parse_application') as mock_parse:
            mock_parse.return_value = {
                "household": {"address": "123 Main St"},
                "drivers": [{"name": "John Doe", "age": 30, "license_years": 10}],
                "vehicles": [{"make": "Toyota", "model": "Camry", "year": 2020}],
                "issues": []
            }
            
            with patch('src.agents.risk_factor_agent.assess') as mock_assess:
                mock_assess.return_value = {
                    "risk_factor": "three_year_claim_free_discount",
                    "overall_risk_tier": "LOW",
                    "confidence": 0.85
                }
                
                result = engine.process_application_with_graph(sample_application)
                
                assert result.status == "completed"
                assert result.session_id is not None
                assert len(result.execution_order) > 0
                assert result.execution_time_ms > 0
                
    def test_execution_history(self):
        """Test execution history management."""
        engine = create_rating_engine()
        
        # Initially empty
        history = engine.get_execution_history()
        assert len(history) == 0
        
        # After processing (mocked)
        sample_application = json.dumps({"test": "data"})
        
        with patch('src.agents.orchestrator_agent.parse_application') as mock_parse:
            mock_parse.return_value = {"test": "data", "issues": []}
            
            with patch('src.agents.risk_factor_agent.assess') as mock_assess:
                mock_assess.return_value = {"risk_factor": "test", "confidence": 0.8}
                
                engine.process_application_with_graph(sample_application)
                
        history = engine.get_execution_history()
        assert len(history) == 1
        
        # Test history limit
        limited_history = engine.get_execution_history(limit=1)
        assert len(limited_history) == 1
        
        # Test clear history
        engine.clear_execution_history()
        history = engine.get_execution_history()
        assert len(history) == 0


class TestMultiAgentIntegration:
    """Integration tests for the complete multi-agent system."""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        engine = create_rating_engine("Monthly-Comfort")
        
        # Sample application data
        sample_application = {
            "household": {
                "address": "123 Main St, Anytown, USA",
                "zip_code": "12345"
            },
            "drivers": [
                {
                    "name": "John Doe",
                    "age": 35,
                    "gender": "M",
                    "marital_status": "married",
                    "license_years": 15,
                    "violations": [],
                    "claims": []
                }
            ],
            "vehicles": [
                {
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2020,
                    "vin": "1234567890ABCDEF",
                    "usage": "commuting"
                }
            ]
        }
        
        with patch('src.agents.orchestrator_agent.parse_application') as mock_parse:
            mock_parse.return_value = {
                **sample_application,
                "issues": []
            }
            
            with patch('src.agents.risk_factor_agent.assess') as mock_assess:
                mock_assess.return_value = {
                    "risk_factor": "three_year_claim_free_discount",
                    "overall_risk_tier": "LOW",
                    "key_factors": ["clean_driving_record", "experienced_driver"],
                    "confidence": 0.9,
                    "reasoning_steps": [
                        {"step": "Analyzed driving record", "rationale": "No violations or claims"}
                    ]
                }
                
                result = engine.process_application_with_graph(json.dumps(sample_application))
                
                # Verify result structure
                assert result.status == "completed"
                assert result.session_id is not None
                assert result.risk_profile is not None
                assert result.risk_assessment is not None
                assert result.premium_calculation is not None
                assert len(result.execution_order) > 0
                assert result.execution_time_ms > 0
                assert len(result.errors) == 0
                
                # Verify execution order follows architecture
                expected_order = ["product_definition", "risk_reasoning", "data_lookup", "premium_calculation"]
                assert all(step in result.execution_order for step in expected_order)
                
    def test_error_handling(self):
        """Test error handling in multi-agent workflow."""
        engine = create_rating_engine("Monthly-Comfort")
        
        # Test with invalid application data
        invalid_application = "invalid json"
        
        result = engine.process_application_with_graph(invalid_application)
        
        assert result.status == "failed"
        assert len(result.errors) > 0
        
    def test_product_variation(self):
        """Test workflow with different product codes."""
        products = ["Monthly-Economy", "Monthly-Comfort", "Monthly-Turbo"]
        
        for product_code in products:
            engine = create_rating_engine(product_code)
            status = engine.get_graph_status()
            assert status["product_code"] == product_code
            
            # Test product definition exists
            product_def = engine.product_agent.get_product_definition(product_code)
            assert product_def is not None
            assert product_def.product_code == product_code
