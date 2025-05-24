"""
GOTS (Global Organic Textile Standard) Compliance Checker

This module ensures all material recommendations meet organic certification
standards for fibers, processing methods, and chemical treatments.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class GOTSLimits:
    """GOTS certification limits and requirements."""
    
    # Approved organic fibers
    APPROVED_FIBERS = [
        'cotton', 'wool', 'silk', 'hemp', 'flax', 'linen',
        'jute', 'kapok', 'ramie', 'coir', 'sisal'
    ]
    
    # Fiber-specific temperature limits (°C)
    MAX_PROCESSING_TEMP = {
        'cotton': 150,
        'wool': 120,
        'silk': 110,
        'hemp': 160,
        'flax': 150,
        'linen': 150,
        'jute': 140,
        'kapok': 130,
        'ramie': 150,
        'coir': 140,
        'sisal': 145
    }
    
    # Approved processing chemicals
    APPROVED_CHEMICALS = [
        'hydrogen_peroxide',
        'citric_acid',
        'acetic_acid',
        'formic_acid',
        'oxalic_acid',
        'natural_enzymes',
        'sodium_carbonate',
        'sodium_bicarbonate',
        'natural_soap',
        'plant_based_surfactants'
    ]
    
    # Prohibited chemicals
    PROHIBITED_CHEMICALS = [
        'formaldehyde',
        'chlorine_bleach',
        'azo_dyes',
        'heavy_metals',
        'phthalates',
        'pfas',
        'organotin_compounds',
        'chlorophenols',
        'chlorobenzenes'
    ]
    
    # Environmental limits
    MAX_WATER_CONSUMPTION = 100  # L/kg
    MAX_ENERGY_CONSUMPTION = 10  # kWh/kg
    MIN_ORGANIC_CONTENT = 0.70  # 70% for "made with organic" label
    MIN_ORGANIC_CONTENT_FULL = 0.95  # 95% for "organic" label
    
    # Additional requirements
    REQUIRES_MULESING_FREE_WOOL = True
    REQUIRES_NON_GMO = True
    REQUIRES_SOCIAL_CRITERIA = True


class GOTSComplianceChecker:
    """Check and ensure GOTS compliance for material recommendations."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.limits = GOTSLimits()
        
        # Load custom configuration if provided
        if config_path:
            self._load_custom_config(config_path)
            
    def _load_custom_config(self, config_path: str):
        """Load custom GOTS configuration from file."""
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        # Update limits with custom values
        for key, value in config.items():
            if hasattr(self.limits, key):
                setattr(self.limits, key, value)
                
    def check_fiber_compliance(self, fiber_type: str) -> Tuple[bool, str]:
        """
        Check if a fiber type is GOTS approved.
        
        Args:
            fiber_type: Name of the fiber
            
        Returns:
            Tuple of (is_compliant, reason)
        """
        fiber_lower = fiber_type.lower().strip()
        
        if fiber_lower not in self.limits.APPROVED_FIBERS:
            return False, f"Fiber '{fiber_type}' is not GOTS approved"
            
        return True, "Fiber is GOTS approved"
    
    def check_processing_temperature(self, 
                                   fiber_composition: Dict[str, float],
                                   processing_temp: float) -> Tuple[bool, str]:
        """
        Check if processing temperature is within GOTS limits.
        
        Args:
            fiber_composition: Dict mapping fiber types to percentages
            processing_temp: Processing temperature in °C
            
        Returns:
            Tuple of (is_compliant, reason)
        """
        # Find the most restrictive temperature limit
        min_allowed_temp = float('inf')
        limiting_fiber = None
        
        for fiber, percentage in fiber_composition.items():
            if percentage > 0:
                fiber_lower = fiber.lower().strip()
                if fiber_lower in self.limits.MAX_PROCESSING_TEMP:
                    temp_limit = self.limits.MAX_PROCESSING_TEMP[fiber_lower]
                    if temp_limit < min_allowed_temp:
                        min_allowed_temp = temp_limit
                        limiting_fiber = fiber
                        
        if processing_temp > min_allowed_temp:
            return False, (f"Processing temperature {processing_temp}°C exceeds "
                          f"limit of {min_allowed_temp}°C for {limiting_fiber}")
                          
        return True, "Processing temperature is within GOTS limits"
    
    def check_chemical_compliance(self, chemicals: List[str]) -> Tuple[bool, str]:
        """
        Check if all chemicals are GOTS approved.
        
        Args:
            chemicals: List of chemical names
            
        Returns:
            Tuple of (is_compliant, reason)
        """
        non_compliant = []
        
        for chemical in chemicals:
            chemical_lower = chemical.lower().strip().replace(' ', '_')
            
            # Check if prohibited
            if chemical_lower in self.limits.PROHIBITED_CHEMICALS:
                return False, f"Chemical '{chemical}' is prohibited by GOTS"
                
            # Check if not approved
            if chemical_lower not in self.limits.APPROVED_CHEMICALS:
                non_compliant.append(chemical)
                
        if non_compliant:
            return False, f"Chemicals not GOTS approved: {', '.join(non_compliant)}"
            
        return True, "All chemicals are GOTS approved"
    
    def check_organic_content(self, 
                            fiber_composition: Dict[str, float],
                            label_grade: str = "made_with_organic") -> Tuple[bool, str]:
        """
        Check if organic content meets GOTS requirements.
        
        Args:
            fiber_composition: Dict mapping fiber types to percentages
            label_grade: Either "organic" or "made_with_organic"
            
        Returns:
            Tuple of (is_compliant, reason)
        """
        # Calculate total organic content
        organic_content = sum(fiber_composition.values())
        
        if label_grade == "organic":
            min_content = self.limits.MIN_ORGANIC_CONTENT_FULL
            label = "organic"
        else:
            min_content = self.limits.MIN_ORGANIC_CONTENT
            label = "made with organic"
            
        if organic_content < min_content:
            return False, (f"Organic content {organic_content:.1%} is below "
                          f"{min_content:.0%} required for '{label}' label")
                          
        return True, f"Organic content meets requirements for '{label}' label"
    
    def check_environmental_impact(self,
                                 water_consumption: float,
                                 energy_consumption: float) -> Tuple[bool, str]:
        """
        Check if environmental impact is within GOTS limits.
        
        Args:
            water_consumption: Water usage in L/kg
            energy_consumption: Energy usage in kWh/kg
            
        Returns:
            Tuple of (is_compliant, reason)
        """
        issues = []
        
        if water_consumption > self.limits.MAX_WATER_CONSUMPTION:
            issues.append(f"Water consumption {water_consumption} L/kg exceeds "
                         f"limit of {self.limits.MAX_WATER_CONSUMPTION} L/kg")
                         
        if energy_consumption > self.limits.MAX_ENERGY_CONSUMPTION:
            issues.append(f"Energy consumption {energy_consumption} kWh/kg exceeds "
                         f"limit of {self.limits.MAX_ENERGY_CONSUMPTION} kWh/kg")
                         
        if issues:
            return False, "; ".join(issues)
            
        return True, "Environmental impact is within GOTS limits"
    
    def check_full_compliance(self, recommendation: Dict) -> Dict[str, Tuple[bool, str]]:
        """
        Perform comprehensive GOTS compliance check.
        
        Args:
            recommendation: Dict containing:
                - fiber_composition: Dict[str, float]
                - processing_temp: float
                - chemicals: List[str]
                - water_consumption: float
                - energy_consumption: float
                - label_grade: str
                
        Returns:
            Dict mapping check names to (is_compliant, reason) tuples
        """
        results = {}
        
        # Check each fiber
        for fiber in recommendation.get('fiber_composition', {}):
            is_compliant, reason = self.check_fiber_compliance(fiber)
            results[f'fiber_{fiber}'] = (is_compliant, reason)
            
        # Check processing temperature
        if 'processing_temp' in recommendation:
            results['processing_temp'] = self.check_processing_temperature(
                recommendation['fiber_composition'],
                recommendation['processing_temp']
            )
            
        # Check chemicals
        if 'chemicals' in recommendation:
            results['chemicals'] = self.check_chemical_compliance(
                recommendation['chemicals']
            )
            
        # Check organic content
        results['organic_content'] = self.check_organic_content(
            recommendation.get('fiber_composition', {}),
            recommendation.get('label_grade', 'made_with_organic')
        )
        
        # Check environmental impact
        if 'water_consumption' in recommendation and 'energy_consumption' in recommendation:
            results['environmental'] = self.check_environmental_impact(
                recommendation['water_consumption'],
                recommendation['energy_consumption']
            )
            
        return results
    
    def generate_compliance_report(self, recommendation: Dict) -> str:
        """Generate a human-readable compliance report."""
        results = self.check_full_compliance(recommendation)
        
        report = ["GOTS Compliance Report", "=" * 50, ""]
        
        # Summary
        compliant_checks = sum(1 for is_compliant, _ in results.values() if is_compliant)
        total_checks = len(results)
        
        if compliant_checks == total_checks:
            report.append("✓ FULLY GOTS COMPLIANT")
        else:
            report.append(f"⚠ COMPLIANCE ISSUES: {total_checks - compliant_checks} of {total_checks} checks failed")
            
        report.append("")
        
        # Detailed results
        for check_name, (is_compliant, reason) in results.items():
            status = "✓" if is_compliant else "✗"
            report.append(f"{status} {check_name}: {reason}")
            
        return "\n".join(report)
    
    def suggest_modifications(self, recommendation: Dict) -> List[str]:
        """Suggest modifications to make a recommendation GOTS compliant."""
        suggestions = []
        results = self.check_full_compliance(recommendation)
        
        for check_name, (is_compliant, reason) in results.items():
            if not is_compliant:
                if 'temperature' in reason:
                    suggestions.append("Reduce processing temperature or change fiber composition")
                elif 'chemical' in reason:
                    suggestions.append("Replace non-approved chemicals with GOTS-approved alternatives")
                elif 'organic content' in reason:
                    suggestions.append("Increase organic fiber content")
                elif 'water' in reason:
                    suggestions.append("Optimize process to reduce water consumption")
                elif 'energy' in reason:
                    suggestions.append("Implement energy-efficient processing methods")
                    
        return suggestions


def validate_gots_batch(recommendations: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Validate a batch of recommendations for GOTS compliance.
    
    Args:
        recommendations: List of recommendation dictionaries
        
    Returns:
        Tuple of (compliant_recommendations, non_compliant_recommendations)
    """
    checker = GOTSComplianceChecker()
    compliant = []
    non_compliant = []
    
    for rec in recommendations:
        results = checker.check_full_compliance(rec)
        
        # Check if all checks passed
        if all(is_compliant for is_compliant, _ in results.values()):
            compliant.append(rec)
        else:
            non_compliant.append(rec)
            
    return compliant, non_compliant 