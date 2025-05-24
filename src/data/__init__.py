"""
Synthetic Plastic Transformer - Data Module

Contains dataset classes and natural fiber property databases.
"""

from .fiber_polymer_dataset import FiberPolymerDataset, PolymerGraphDataset
from .natural_fiber_properties import (
    FiberProperties,
    NATURAL_FIBER_DATABASE,
    get_fiber_properties,
    get_property_ranges,
    find_fibers_by_property,
    calculate_blend_properties
)

__all__ = [
    'FiberPolymerDataset',
    'PolymerGraphDataset',
    'FiberProperties',
    'NATURAL_FIBER_DATABASE',
    'get_fiber_properties',
    'get_property_ranges',
    'find_fibers_by_property',
    'calculate_blend_properties'
]
