"""
Unit tests for GOTS compliance checking functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from utils.gots_compliance import GOTSComplianceChecker, GOTSLimits


class TestGOTSComplianceChecker:
    """Test cases for GOTS compliance checking."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.checker = GOTSComplianceChecker()
        
    def test_fiber_compliance(self):
        """Test fiber type compliance checking."""
        # Test approved fibers
        approved_fibers = ['cotton', 'wool', 'silk', 'hemp', 'flax', 'jute']
        for fiber in approved_fibers:
            is_compliant, reason = self.checker.check_fiber_compliance(fiber)
            assert is_compliant, f"{fiber} should be GOTS approved"
            
        # Test non-approved fibers
        non_approved = ['polyester', 'nylon', 'acrylic']
        for fiber in non_approved:
            is_compliant, reason = self.checker.check_fiber_compliance(fiber)
            assert not is_compliant, f"{fiber} should not be GOTS approved"
            
    def test_processing_temperature(self):
        """Test processing temperature compliance."""
        # Test within limits
        fiber_comp = {'cotton': 0.5, 'hemp': 0.5}
        is_compliant, reason = self.checker.check_processing_temperature(fiber_comp, 140)
        assert is_compliant, "Temperature should be within limits"
        
        # Test exceeding limits
        is_compliant, reason = self.checker.check_processing_temperature(fiber_comp, 170)
        assert not is_compliant, "Temperature should exceed limits"
        
        # Test with wool (lower temp limit)
        fiber_comp_wool = {'wool': 0.5, 'cotton': 0.5}
        is_compliant, reason = self.checker.check_processing_temperature(fiber_comp_wool, 130)
        assert not is_compliant, "Temperature should exceed wool limit"
        
    def test_chemical_compliance(self):
        """Test chemical compliance checking."""
        # Test approved chemicals
        approved = ['hydrogen_peroxide', 'citric_acid', 'natural_enzymes']
        is_compliant, reason = self.checker.check_chemical_compliance(approved)
        assert is_compliant, "Approved chemicals should pass"
        
        # Test prohibited chemicals
        prohibited = ['hydrogen_peroxide', 'formaldehyde']
        is_compliant, reason = self.checker.check_chemical_compliance(prohibited)
        assert not is_compliant, "Prohibited chemicals should fail"
        assert 'formaldehyde' in reason
        
        # Test non-approved chemicals
        non_approved = ['hydrogen_peroxide', 'unknown_chemical']
        is_compliant, reason = self.checker.check_chemical_compliance(non_approved)
        assert not is_compliant, "Non-approved chemicals should fail"
        
    def test_organic_content(self):
        """Test organic content requirements."""
        # Test "made with organic" label (70% minimum)
        fiber_comp_70 = {'cotton': 0.7, 'synthetic': 0.3}
        is_compliant, reason = self.checker.check_organic_content(
            fiber_comp_70, 'made_with_organic'
        )
        assert is_compliant, "70% organic should pass for 'made with organic'"
        
        # Test below threshold
        fiber_comp_60 = {'cotton': 0.6, 'synthetic': 0.4}
        is_compliant, reason = self.checker.check_organic_content(
            fiber_comp_60, 'made_with_organic'
        )
        assert not is_compliant, "60% organic should fail"
        
        # Test "organic" label (95% minimum)
        fiber_comp_95 = {'cotton': 0.95, 'synthetic': 0.05}
        is_compliant, reason = self.checker.check_organic_content(
            fiber_comp_95, 'organic'
        )
        assert is_compliant, "95% organic should pass for 'organic' label"
        
    def test_environmental_impact(self):
        """Test environmental impact limits."""
        # Test within limits
        is_compliant, reason = self.checker.check_environmental_impact(80, 8)
        assert is_compliant, "Should be within environmental limits"
        
        # Test exceeding water limit
        is_compliant, reason = self.checker.check_environmental_impact(120, 8)
        assert not is_compliant, "Should exceed water limit"
        assert 'Water consumption' in reason
        
        # Test exceeding energy limit
        is_compliant, reason = self.checker.check_environmental_impact(80, 12)
        assert not is_compliant, "Should exceed energy limit"
        assert 'Energy consumption' in reason
        
    def test_full_compliance_check(self):
        """Test comprehensive compliance checking."""
        # Fully compliant recommendation
        recommendation = {
            'fiber_composition': {'cotton': 0.5, 'hemp': 0.3, 'wool': 0.2},
            'processing_temp': 110,
            'chemicals': ['hydrogen_peroxide', 'citric_acid'],
            'water_consumption': 80,
            'energy_consumption': 8,
            'label_grade': 'organic'
        }
        
        results = self.checker.check_full_compliance(recommendation)
        
        # Check all individual results
        assert results['fiber_cotton'][0], "Cotton should be compliant"
        assert results['fiber_hemp'][0], "Hemp should be compliant"
        assert results['fiber_wool'][0], "Wool should be compliant"
        assert results['processing_temp'][0], "Temperature should be compliant"
        assert results['chemicals'][0], "Chemicals should be compliant"
        assert results['organic_content'][0], "Organic content should be compliant"
        assert results['environmental'][0], "Environmental impact should be compliant"
        
    def test_compliance_report_generation(self):
        """Test compliance report generation."""
        recommendation = {
            'fiber_composition': {'cotton': 0.8, 'hemp': 0.2},
            'processing_temp': 140,
            'chemicals': ['hydrogen_peroxide'],
            'water_consumption': 90,
            'energy_consumption': 9,
            'label_grade': 'made_with_organic'
        }
        
        report = self.checker.generate_compliance_report(recommendation)
        
        assert "FULLY GOTS COMPLIANT" in report
        assert "✓" in report
        assert "✗" not in report
        
    def test_modification_suggestions(self):
        """Test suggestions for non-compliant recommendations."""
        # Non-compliant recommendation
        recommendation = {
            'fiber_composition': {'cotton': 0.5, 'polyester': 0.5},
            'processing_temp': 180,
            'chemicals': ['formaldehyde'],
            'water_consumption': 150,
            'energy_consumption': 15
        }
        
        suggestions = self.checker.suggest_modifications(recommendation)
        
        assert any('temperature' in s.lower() for s in suggestions)
        assert any('chemical' in s.lower() for s in suggestions)
        assert any('water' in s.lower() for s in suggestions)
        assert any('energy' in s.lower() for s in suggestions)


def test_gots_limits_dataclass():
    """Test GOTSLimits dataclass."""
    limits = GOTSLimits()
    
    assert 'cotton' in limits.APPROVED_FIBERS
    assert limits.MAX_WATER_CONSUMPTION == 100
    assert limits.MIN_ORGANIC_CONTENT == 0.70
    assert limits.REQUIRES_NON_GMO == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 