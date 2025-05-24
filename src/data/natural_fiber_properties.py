"""
Natural Fiber Properties Database

Comprehensive database of natural fiber properties including mechanical,
thermal, moisture, and processing characteristics based on literature data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class FiberProperties:
    """Complete properties for a natural fiber type."""
    
    # Basic properties
    name: str
    fiber_type: str  # bast, leaf, seed, protein
    
    # Mechanical properties (ranges)
    tensile_strength: Tuple[float, float]  # MPa
    elastic_modulus: Tuple[float, float]  # GPa
    elongation_at_break: Tuple[float, float]  # %
    
    # Physical properties
    density: float  # g/cm³
    diameter: Tuple[float, float]  # μm
    length: Tuple[float, float]  # mm
    aspect_ratio: Tuple[float, float]
    
    # Chemical composition (%)
    cellulose: float
    hemicellulose: float
    lignin: float
    pectin: float
    wax: float
    moisture_content: float
    
    # Thermal properties
    thermal_conductivity: float  # W/mK
    specific_heat: float  # J/gK
    thermal_stability: float  # °C
    glass_transition: Optional[float]  # °C
    
    # Moisture properties
    moisture_regain: float  # %
    water_absorption: float  # %
    contact_angle: float  # degrees
    
    # Environmental properties
    biodegradability_rate: float  # 0-1 scale
    carbon_footprint: float  # kg CO2/kg
    water_usage: float  # L/kg
    
    # Processing properties
    alkali_resistance: float  # 0-1 scale
    enzyme_compatibility: float  # 0-1 scale
    dye_affinity: float  # 0-1 scale
    
    # Special properties
    antimicrobial: bool
    uv_resistance: float  # 0-1 scale
    flame_resistance: float  # 0-1 scale
    
    # GOTS certification
    gots_certified: bool
    organic_sources: List[str]


# Comprehensive fiber database based on literature values
NATURAL_FIBER_DATABASE = {
    'cotton': FiberProperties(
        name='Cotton',
        fiber_type='seed',
        tensile_strength=(287, 800),
        elastic_modulus=(5.5, 12.6),
        elongation_at_break=(3, 10),
        density=1.54,
        diameter=(12, 20),
        length=(10, 60),
        aspect_ratio=(1000, 3000),
        cellulose=82.7,
        hemicellulose=5.7,
        lignin=0.0,
        pectin=5.7,
        wax=0.6,
        moisture_content=8.5,
        thermal_conductivity=0.026,
        specific_heat=1.34,
        thermal_stability=150,
        glass_transition=None,
        moisture_regain=8.5,
        water_absorption=20,
        contact_angle=0,  # Hydrophilic
        biodegradability_rate=0.95,
        carbon_footprint=3.8,
        water_usage=10000,
        alkali_resistance=0.8,
        enzyme_compatibility=0.9,
        dye_affinity=0.9,
        antimicrobial=False,
        uv_resistance=0.3,
        flame_resistance=0.2,
        gots_certified=True,
        organic_sources=['USA', 'India', 'Turkey']
    ),
    
    'hemp': FiberProperties(
        name='Hemp',
        fiber_type='bast',
        tensile_strength=(550, 1110),
        elastic_modulus=(30, 80),
        elongation_at_break=(1.6, 4.0),
        density=1.48,
        diameter=(15, 50),
        length=(5, 55),
        aspect_ratio=(1000, 2000),
        cellulose=70.2,
        hemicellulose=22.4,
        lignin=3.7,
        pectin=0.9,
        wax=0.8,
        moisture_content=12.0,
        thermal_conductivity=0.040,
        specific_heat=1.40,
        thermal_stability=160,
        glass_transition=None,
        moisture_regain=12.0,
        water_absorption=30,
        contact_angle=20,
        biodegradability_rate=0.98,
        carbon_footprint=0.7,
        water_usage=2700,
        alkali_resistance=0.9,
        enzyme_compatibility=0.8,
        dye_affinity=0.7,
        antimicrobial=True,
        uv_resistance=0.8,
        flame_resistance=0.4,
        gots_certified=True,
        organic_sources=['Canada', 'France', 'Netherlands']
    ),
    
    'flax': FiberProperties(
        name='Flax (Linen)',
        fiber_type='bast',
        tensile_strength=(345, 1500),
        elastic_modulus=(27.6, 80),
        elongation_at_break=(1.2, 3.2),
        density=1.50,
        diameter=(12, 30),
        length=(20, 100),
        aspect_ratio=(1200, 3000),
        cellulose=71.0,
        hemicellulose=18.6,
        lignin=2.2,
        pectin=2.3,
        wax=1.7,
        moisture_content=12.0,
        thermal_conductivity=0.037,
        specific_heat=1.38,
        thermal_stability=150,
        glass_transition=None,
        moisture_regain=12.0,
        water_absorption=25,
        contact_angle=15,
        biodegradability_rate=0.97,
        carbon_footprint=0.5,
        water_usage=2500,
        alkali_resistance=0.85,
        enzyme_compatibility=0.85,
        dye_affinity=0.75,
        antimicrobial=True,
        uv_resistance=0.7,
        flame_resistance=0.3,
        gots_certified=True,
        organic_sources=['Belgium', 'France', 'Belarus']
    ),
    
    'jute': FiberProperties(
        name='Jute',
        fiber_type='bast',
        tensile_strength=(393, 800),
        elastic_modulus=(10, 30),
        elongation_at_break=(1.5, 1.8),
        density=1.46,
        diameter=(15, 25),
        length=(1.5, 4),
        aspect_ratio=(100, 250),
        cellulose=61.0,
        hemicellulose=14.0,
        lignin=12.0,
        pectin=0.2,
        wax=0.5,
        moisture_content=13.75,
        thermal_conductivity=0.035,
        specific_heat=1.35,
        thermal_stability=140,
        glass_transition=None,
        moisture_regain=13.75,
        water_absorption=35,
        contact_angle=25,
        biodegradability_rate=0.99,
        carbon_footprint=0.4,
        water_usage=2000,
        alkali_resistance=0.7,
        enzyme_compatibility=0.8,
        dye_affinity=0.8,
        antimicrobial=False,
        uv_resistance=0.5,
        flame_resistance=0.3,
        gots_certified=True,
        organic_sources=['India', 'Bangladesh']
    ),
    
    'silk': FiberProperties(
        name='Silk',
        fiber_type='protein',
        tensile_strength=(300, 740),
        elastic_modulus=(7, 17),
        elongation_at_break=(10, 25),
        density=1.34,
        diameter=(10, 14),
        length=(1000, 1500),  # Continuous filament
        aspect_ratio=(100000, 150000),
        cellulose=0.0,
        hemicellulose=0.0,
        lignin=0.0,
        pectin=0.0,
        wax=0.0,
        moisture_content=11.0,
        thermal_conductivity=0.055,
        specific_heat=1.38,
        thermal_stability=110,
        glass_transition=175,
        moisture_regain=11.0,
        water_absorption=30,
        contact_angle=50,
        biodegradability_rate=0.85,
        carbon_footprint=5.5,
        water_usage=5000,
        alkali_resistance=0.4,
        enzyme_compatibility=0.6,
        dye_affinity=0.95,
        antimicrobial=False,
        uv_resistance=0.4,
        flame_resistance=0.6,
        gots_certified=True,
        organic_sources=['China', 'India', 'Thailand']
    ),
    
    'wool': FiberProperties(
        name='Wool',
        fiber_type='protein',
        tensile_strength=(104, 212),
        elastic_modulus=(2.3, 5.0),
        elongation_at_break=(25, 35),
        density=1.32,
        diameter=(15, 40),
        length=(50, 150),
        aspect_ratio=(2000, 10000),
        cellulose=0.0,
        hemicellulose=0.0,
        lignin=0.0,
        pectin=0.0,
        wax=0.5,
        moisture_content=13.0,
        thermal_conductivity=0.034,
        specific_heat=1.36,
        thermal_stability=120,
        glass_transition=144,
        moisture_regain=13.0,
        water_absorption=35,
        contact_angle=110,  # Hydrophobic due to lanolin
        biodegradability_rate=0.80,
        carbon_footprint=6.2,
        water_usage=6000,
        alkali_resistance=0.3,
        enzyme_compatibility=0.5,
        dye_affinity=0.98,
        antimicrobial=True,
        uv_resistance=0.3,
        flame_resistance=0.8,
        gots_certified=True,
        organic_sources=['Australia', 'New Zealand', 'Uruguay']
    ),
    
    'bamboo': FiberProperties(
        name='Bamboo (Mechanical)',
        fiber_type='bast',
        tensile_strength=(441, 610),
        elastic_modulus=(11, 32),
        elongation_at_break=(2.5, 3.7),
        density=1.50,
        diameter=(10, 40),
        length=(1.5, 4),
        aspect_ratio=(100, 400),
        cellulose=73.8,
        hemicellulose=12.5,
        lignin=10.2,
        pectin=0.4,
        wax=0.5,
        moisture_content=11.0,
        thermal_conductivity=0.032,
        specific_heat=1.39,
        thermal_stability=140,
        glass_transition=None,
        moisture_regain=11.0,
        water_absorption=40,
        contact_angle=30,
        biodegradability_rate=0.96,
        carbon_footprint=0.3,
        water_usage=1500,
        alkali_resistance=0.75,
        enzyme_compatibility=0.85,
        dye_affinity=0.7,
        antimicrobial=True,
        uv_resistance=0.7,
        flame_resistance=0.3,
        gots_certified=False,  # Mechanical bamboo can be certified
        organic_sources=['China', 'India']
    ),
    
    'sisal': FiberProperties(
        name='Sisal',
        fiber_type='leaf',
        tensile_strength=(468, 700),
        elastic_modulus=(9.4, 38),
        elongation_at_break=(2, 7),
        density=1.45,
        diameter=(100, 300),
        length=(0.6, 1.5),
        aspect_ratio=(5, 15),
        cellulose=67.0,
        hemicellulose=12.0,
        lignin=8.0,
        pectin=10.0,
        wax=2.0,
        moisture_content=11.0,
        thermal_conductivity=0.042,
        specific_heat=1.33,
        thermal_stability=145,
        glass_transition=None,
        moisture_regain=11.0,
        water_absorption=60,
        contact_angle=35,
        biodegradability_rate=0.97,
        carbon_footprint=0.6,
        water_usage=1800,
        alkali_resistance=0.8,
        enzyme_compatibility=0.7,
        dye_affinity=0.6,
        antimicrobial=False,
        uv_resistance=0.5,
        flame_resistance=0.3,
        gots_certified=True,
        organic_sources=['Brazil', 'Tanzania', 'Kenya']
    ),
    
    'coir': FiberProperties(
        name='Coir',
        fiber_type='seed',
        tensile_strength=(131, 220),
        elastic_modulus=(4, 6),
        elongation_at_break=(15, 40),
        density=1.15,
        diameter=(100, 450),
        length=(0.3, 1.0),
        aspect_ratio=(2, 10),
        cellulose=36.0,
        hemicellulose=0.25,
        lignin=41.0,
        pectin=3.0,
        wax=0.0,
        moisture_content=8.0,
        thermal_conductivity=0.047,
        specific_heat=1.28,
        thermal_stability=130,
        glass_transition=None,
        moisture_regain=8.0,
        water_absorption=130,
        contact_angle=90,
        biodegradability_rate=0.70,
        carbon_footprint=0.2,
        water_usage=500,
        alkali_resistance=0.9,
        enzyme_compatibility=0.4,
        dye_affinity=0.4,
        antimicrobial=True,
        uv_resistance=0.6,
        flame_resistance=0.4,
        gots_certified=True,
        organic_sources=['India', 'Sri Lanka', 'Philippines']
    ),
    
    'kapok': FiberProperties(
        name='Kapok',
        fiber_type='seed',
        tensile_strength=(45, 64),
        elastic_modulus=(0.4, 0.8),
        elongation_at_break=(1.8, 4.2),
        density=0.384,  # Very lightweight
        diameter=(20, 40),
        length=(8, 35),
        aspect_ratio=(200, 1750),
        cellulose=64.0,
        hemicellulose=23.0,
        lignin=13.0,
        pectin=0.0,
        wax=0.0,
        moisture_content=0.0,  # Hydrophobic
        thermal_conductivity=0.034,
        specific_heat=1.25,
        thermal_stability=130,
        glass_transition=None,
        moisture_regain=0.0,
        water_absorption=0.0,
        contact_angle=140,  # Highly hydrophobic
        biodegradability_rate=0.60,
        carbon_footprint=0.3,
        water_usage=200,
        alkali_resistance=0.5,
        enzyme_compatibility=0.3,
        dye_affinity=0.2,
        antimicrobial=False,
        uv_resistance=0.4,
        flame_resistance=0.2,
        gots_certified=True,
        organic_sources=['Indonesia', 'Thailand', 'India']
    ),
    
    'ramie': FiberProperties(
        name='Ramie',
        fiber_type='bast',
        tensile_strength=(400, 938),
        elastic_modulus=(44, 128),
        elongation_at_break=(1.2, 3.8),
        density=1.55,
        diameter=(20, 80),
        length=(40, 260),
        aspect_ratio=(1000, 13000),
        cellulose=68.6,
        hemicellulose=13.1,
        lignin=0.6,
        pectin=1.9,
        wax=0.3,
        moisture_content=8.0,
        thermal_conductivity=0.039,
        specific_heat=1.32,
        thermal_stability=150,
        glass_transition=None,
        moisture_regain=8.0,
        water_absorption=25,
        contact_angle=20,
        biodegradability_rate=0.95,
        carbon_footprint=0.6,
        water_usage=2200,
        alkali_resistance=0.95,
        enzyme_compatibility=0.7,
        dye_affinity=0.6,
        antimicrobial=True,
        uv_resistance=0.6,
        flame_resistance=0.3,
        gots_certified=True,
        organic_sources=['China', 'Brazil', 'Philippines']
    ),
    
    'pineapple': FiberProperties(
        name='Pineapple Leaf (PALF)',
        fiber_type='leaf',
        tensile_strength=(170, 1627),
        elastic_modulus=(34.5, 82.5),
        elongation_at_break=(0.8, 3.0),
        density=1.44,
        diameter=(20, 80),
        length=(3, 9),
        aspect_ratio=(50, 450),
        cellulose=70.0,
        hemicellulose=18.0,
        lignin=5.0,
        pectin=2.0,
        wax=3.0,
        moisture_content=11.8,
        thermal_conductivity=0.038,
        specific_heat=1.34,
        thermal_stability=140,
        glass_transition=None,
        moisture_regain=11.8,
        water_absorption=45,
        contact_angle=40,
        biodegradability_rate=0.94,
        carbon_footprint=0.1,  # Agricultural waste
        water_usage=100,  # Agricultural waste
        alkali_resistance=0.7,
        enzyme_compatibility=0.8,
        dye_affinity=0.65,
        antimicrobial=False,
        uv_resistance=0.55,
        flame_resistance=0.25,
        gots_certified=False,  # Can be certified if organic
        organic_sources=['Philippines', 'Thailand', 'Indonesia']
    ),
    
    'banana': FiberProperties(
        name='Banana Fiber',
        fiber_type='bast',
        tensile_strength=(529, 914),
        elastic_modulus=(27, 32),
        elongation_at_break=(3.5, 5.9),
        density=1.35,
        diameter=(50, 250),
        length=(0.4, 1.2),
        aspect_ratio=(4, 24),
        cellulose=63.0,
        hemicellulose=19.0,
        lignin=5.0,
        pectin=0.0,
        wax=0.0,
        moisture_content=10.0,
        thermal_conductivity=0.041,
        specific_heat=1.30,
        thermal_stability=135,
        glass_transition=None,
        moisture_regain=10.0,
        water_absorption=50,
        contact_angle=45,
        biodegradability_rate=0.93,
        carbon_footprint=0.1,  # Agricultural waste
        water_usage=50,  # Agricultural waste
        alkali_resistance=0.65,
        enzyme_compatibility=0.75,
        dye_affinity=0.7,
        antimicrobial=False,
        uv_resistance=0.5,
        flame_resistance=0.2,
        gots_certified=False,  # Can be certified if organic
        organic_sources=['India', 'Philippines', 'Ecuador']
    )
}


def get_fiber_properties(fiber_name: str) -> Optional[FiberProperties]:
    """Get properties for a specific fiber type."""
    return NATURAL_FIBER_DATABASE.get(fiber_name.lower())


def get_property_ranges() -> pd.DataFrame:
    """Get min/max ranges for all properties across all fibers."""
    ranges = {}
    
    for fiber_name, props in NATURAL_FIBER_DATABASE.items():
        ranges[fiber_name] = {
            'tensile_strength_min': props.tensile_strength[0],
            'tensile_strength_max': props.tensile_strength[1],
            'elastic_modulus_min': props.elastic_modulus[0],
            'elastic_modulus_max': props.elastic_modulus[1],
            'elongation_min': props.elongation_at_break[0],
            'elongation_max': props.elongation_at_break[1],
            'density': props.density,
            'moisture_regain': props.moisture_regain,
            'thermal_conductivity': props.thermal_conductivity,
            'biodegradability': props.biodegradability_rate,
            'carbon_footprint': props.carbon_footprint
        }
        
    return pd.DataFrame(ranges).T


def find_fibers_by_property(property_name: str, 
                           min_value: float,
                           max_value: Optional[float] = None) -> List[str]:
    """Find fibers that meet property criteria."""
    matching_fibers = []
    
    for fiber_name, props in NATURAL_FIBER_DATABASE.items():
        value = getattr(props, property_name, None)
        
        if value is None:
            continue
            
        # Handle tuple properties (ranges)
        if isinstance(value, tuple):
            if max_value:
                if value[0] <= max_value and value[1] >= min_value:
                    matching_fibers.append(fiber_name)
            else:
                if value[1] >= min_value:
                    matching_fibers.append(fiber_name)
        else:
            # Single value properties
            if max_value:
                if min_value <= value <= max_value:
                    matching_fibers.append(fiber_name)
            else:
                if value >= min_value:
                    matching_fibers.append(fiber_name)
                    
    return matching_fibers


def calculate_blend_properties(fiber_ratios: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate estimated properties for a fiber blend.
    
    Uses simple rule of mixtures for most properties.
    """
    blend_props = {}
    
    # Initialize properties
    properties_to_blend = [
        'density', 'cellulose', 'hemicellulose', 'lignin',
        'thermal_conductivity', 'moisture_regain', 'biodegradability_rate',
        'carbon_footprint', 'water_usage'
    ]
    
    for prop in properties_to_blend:
        blend_props[prop] = 0.0
        
    # Calculate weighted averages
    for fiber_name, ratio in fiber_ratios.items():
        fiber = get_fiber_properties(fiber_name)
        if fiber:
            for prop in properties_to_blend:
                value = getattr(fiber, prop, 0)
                blend_props[prop] += value * ratio
                
    # Handle range properties (take weighted average of means)
    for prop_name in ['tensile_strength', 'elastic_modulus', 'elongation_at_break']:
        min_val = 0
        max_val = 0
        
        for fiber_name, ratio in fiber_ratios.items():
            fiber = get_fiber_properties(fiber_name)
            if fiber:
                prop_range = getattr(fiber, prop_name, (0, 0))
                min_val += prop_range[0] * ratio
                max_val += prop_range[1] * ratio
                
        blend_props[f'{prop_name}_min'] = min_val
        blend_props[f'{prop_name}_max'] = max_val
        blend_props[f'{prop_name}_mean'] = (min_val + max_val) / 2
        
    return blend_props 