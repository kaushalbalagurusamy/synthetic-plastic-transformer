"""
Dataset classes for loading and processing fiber and polymer data.

Handles data from multiple sources including PolyInfo, PI1M, and custom
natural fiber databases with GOTS certification information.
"""

import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
import json
from rdkit import Chem
from rdkit.Chem import Descriptors
import h5py
from sklearn.preprocessing import StandardScaler
import logging


class FiberPolymerDataset(Dataset):
    """Dataset for fiber and polymer property data."""
    
    def __init__(self, 
                 data_path: Union[str, Path],
                 mode: str = 'train',
                 transform: Optional[callable] = None,
                 target_properties: Optional[List[str]] = None,
                 augment: bool = True):
        """
        Initialize the dataset.
        
        Args:
            data_path: Path to the data directory
            mode: 'train', 'val', or 'test'
            transform: Optional transform to apply to features
            target_properties: List of properties to predict
            augment: Whether to apply data augmentation
        """
        self.data_path = Path(data_path)
        self.mode = mode
        self.transform = transform
        self.augment = augment
        
        # Default target properties
        if target_properties is None:
            self.target_properties = [
                'tensile_strength', 'elastic_modulus', 'thermal_conductivity',
                'glass_transition_temp', 'water_absorption', 'biodegradability'
            ]
        else:
            self.target_properties = target_properties
            
        # Load data
        self.data = self._load_data()
        
        # Prepare features
        self._prepare_features()
        
        logging.info(f"Loaded {len(self)} samples for {mode} set")
        
    def _load_data(self) -> pd.DataFrame:
        """Load data from various sources."""
        all_data = []
        
        # Load polymer data (PI1M format)
        polymer_file = self.data_path / f'polymers_{self.mode}.csv'
        if polymer_file.exists():
            polymer_data = pd.read_csv(polymer_file)
            polymer_data['material_type'] = 'synthetic_polymer'
            all_data.append(polymer_data)
            
        # Load natural fiber data
        fiber_file = self.data_path / f'fibers_{self.mode}.csv'
        if fiber_file.exists():
            fiber_data = pd.read_csv(fiber_file)
            fiber_data['material_type'] = 'natural_fiber'
            all_data.append(fiber_data)
            
        # Load composite data
        composite_file = self.data_path / f'composites_{self.mode}.csv'
        if composite_file.exists():
            composite_data = pd.read_csv(composite_file)
            composite_data['material_type'] = 'composite'
            all_data.append(composite_data)
            
        # Combine all data
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
        else:
            raise ValueError(f"No data files found in {self.data_path}")
            
        return combined_data
    
    def _prepare_features(self):
        """Prepare molecular and compositional features."""
        self.features = []
        self.targets = []
        self.metadata = []
        
        for idx, row in self.data.iterrows():
            try:
                # Extract features based on material type
                if row['material_type'] == 'synthetic_polymer':
                    features = self._extract_polymer_features(row)
                elif row['material_type'] == 'natural_fiber':
                    features = self._extract_fiber_features(row)
                else:  # composite
                    features = self._extract_composite_features(row)
                    
                # Extract targets
                targets = []
                for prop in self.target_properties:
                    if prop in row:
                        targets.append(row[prop])
                    else:
                        targets.append(np.nan)
                        
                # Store if we have valid features and at least one target
                if features is not None and not all(np.isnan(targets)):
                    self.features.append(features)
                    self.targets.append(np.array(targets))
                    self.metadata.append({
                        'material_id': row.get('material_id', idx),
                        'material_type': row['material_type'],
                        'name': row.get('name', 'Unknown')
                    })
                    
            except Exception as e:
                logging.warning(f"Failed to process row {idx}: {e}")
                
    def _extract_polymer_features(self, row: pd.Series) -> Optional[np.ndarray]:
        """Extract features from polymer SMILES."""
        if 'smiles' not in row or pd.isna(row['smiles']):
            return None
            
        try:
            mol = Chem.MolFromSmiles(row['smiles'])
            if mol is None:
                return None
                
            # Calculate molecular descriptors
            features = [
                Descriptors.MolWt(mol),
                Descriptors.MolLogP(mol),
                Descriptors.NumHAcceptors(mol),
                Descriptors.NumHDonors(mol),
                Descriptors.NumRotatableBonds(mol),
                Descriptors.NumAromaticRings(mol),
                Descriptors.TPSA(mol),
                Descriptors.FractionCsp3(mol),
                Descriptors.NumHeteroatoms(mol),
                Descriptors.RingCount(mol),
                Descriptors.Chi0(mol),
                Descriptors.Chi1(mol)
            ]
            
            # Add custom polymer-specific features
            if 'repeat_unit_mw' in row:
                features.append(row['repeat_unit_mw'])
            else:
                features.append(Descriptors.MolWt(mol))
                
            if 'crystallinity' in row:
                features.append(row['crystallinity'])
            else:
                features.append(0.5)  # Default crystallinity
                
            return np.array(features, dtype=np.float32)
            
        except Exception as e:
            logging.warning(f"Failed to extract polymer features: {e}")
            return None
            
    def _extract_fiber_features(self, row: pd.Series) -> Optional[np.ndarray]:
        """Extract features from natural fiber data."""
        # Chemical composition features
        features = []
        
        # Main components
        for component in ['cellulose', 'hemicellulose', 'lignin', 'pectin', 'wax']:
            if component in row:
                features.append(row[component])
            else:
                features.append(0.0)
                
        # Physical properties
        for prop in ['fiber_diameter', 'fiber_length', 'aspect_ratio', 
                    'density', 'moisture_content']:
            if prop in row:
                features.append(row[prop])
            else:
                features.append(0.0)
                
        # Processing parameters
        for param in ['processing_temp', 'alkali_treatment', 'enzyme_treatment']:
            if param in row:
                features.append(float(row[param]))
            else:
                features.append(0.0)
                
        # GOTS compliance flag
        features.append(1.0 if row.get('gots_certified', False) else 0.0)
        
        return np.array(features, dtype=np.float32)
    
    def _extract_composite_features(self, row: pd.Series) -> Optional[np.ndarray]:
        """Extract features from composite materials."""
        features = []
        
        # Fiber composition (up to 5 components)
        for i in range(5):
            fiber_key = f'fiber_{i}_type'
            ratio_key = f'fiber_{i}_ratio'
            
            if fiber_key in row and ratio_key in row:
                # Encode fiber type
                fiber_encoding = self._encode_fiber_type(row[fiber_key])
                features.extend(fiber_encoding)
                features.append(row[ratio_key])
            else:
                features.extend([0.0] * 8)  # Placeholder for fiber encoding
                features.append(0.0)
                
        # Processing features
        for param in ['processing_temp', 'processing_time', 'pressure']:
            features.append(row.get(param, 0.0))
            
        # Matrix type
        matrix_encoding = self._encode_matrix_type(row.get('matrix_type', 'unknown'))
        features.extend(matrix_encoding)
        
        return np.array(features, dtype=np.float32)
    
    def _encode_fiber_type(self, fiber_type: str) -> List[float]:
        """One-hot encode fiber type."""
        fiber_types = ['cotton', 'wool', 'silk', 'hemp', 'flax', 'jute', 'coir', 'other']
        encoding = [0.0] * len(fiber_types)
        
        fiber_lower = fiber_type.lower() if fiber_type else 'other'
        if fiber_lower in fiber_types:
            encoding[fiber_types.index(fiber_lower)] = 1.0
        else:
            encoding[-1] = 1.0  # Other
            
        return encoding
    
    def _encode_matrix_type(self, matrix_type: str) -> List[float]:
        """Encode matrix/processing type."""
        matrix_types = ['enzymatic', 'alkali', 'mechanical', 'thermal', 'other']
        encoding = [0.0] * len(matrix_types)
        
        matrix_lower = matrix_type.lower() if matrix_type else 'other'
        if matrix_lower in matrix_types:
            encoding[matrix_types.index(matrix_lower)] = 1.0
        else:
            encoding[-1] = 1.0
            
        return encoding
    
    def _augment_sample(self, features: np.ndarray, targets: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Apply data augmentation."""
        if not self.augment or self.mode != 'train':
            return features, targets
            
        # Add Gaussian noise to features
        noise = np.random.normal(0, 0.01, features.shape)
        features_aug = features + noise
        
        # Slightly perturb targets (within measurement uncertainty)
        target_noise = np.random.normal(0, 0.02, targets.shape)
        targets_aug = targets * (1 + target_noise)
        
        return features_aug, targets_aug
    
    def __len__(self) -> int:
        return len(self.features)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        features = self.features[idx].copy()
        targets = self.targets[idx].copy()
        
        # Apply augmentation
        if self.augment:
            features, targets = self._augment_sample(features, targets)
            
        # Apply transform if provided
        if self.transform:
            features = self.transform(features)
            
        return {
            'features': torch.FloatTensor(features),
            'targets': torch.FloatTensor(targets),
            'metadata': self.metadata[idx]
        }


class FiberMixtureDataset(Dataset):
    """Specialized dataset for fiber mixture optimization."""
    
    def __init__(self, base_fibers: List[str], num_mixtures: int = 10000):
        """
        Generate synthetic mixture data for training.
        
        Args:
            base_fibers: List of base fiber types
            num_mixtures: Number of mixtures to generate
        """
        self.base_fibers = base_fibers
        self.num_mixtures = num_mixtures
        
        # Fiber property database (simplified)
        self.fiber_properties = {
            'cotton': {'tensile': 400, 'modulus': 12, 'density': 1.54},
            'hemp': {'tensile': 690, 'modulus': 70, 'density': 1.48},
            'flax': {'tensile': 800, 'modulus': 60, 'density': 1.50},
            'jute': {'tensile': 550, 'modulus': 30, 'density': 1.46},
            'wool': {'tensile': 150, 'modulus': 5, 'density': 1.32},
            'silk': {'tensile': 600, 'modulus': 15, 'density': 1.34},
            'coir': {'tensile': 220, 'modulus': 6, 'density': 1.15},
            'sisal': {'tensile': 600, 'modulus': 38, 'density': 1.45}
        }
        
        # Generate mixtures
        self._generate_mixtures()
        
    def _generate_mixtures(self):
        """Generate random fiber mixtures."""
        self.mixtures = []
        self.properties = []
        
        for _ in range(self.num_mixtures):
            # Random number of components (2-4)
            n_components = np.random.randint(2, 5)
            
            # Select random fibers
            selected_fibers = np.random.choice(
                self.base_fibers, n_components, replace=False
            )
            
            # Generate random ratios that sum to 1
            ratios = np.random.dirichlet(np.ones(n_components))
            
            # Create mixture dict
            mixture = {fiber: ratio for fiber, ratio in zip(selected_fibers, ratios)}
            
            # Calculate mixture properties (simple rule of mixtures)
            mix_props = self._calculate_mixture_properties(mixture)
            
            self.mixtures.append(mixture)
            self.properties.append(mix_props)
            
    def _calculate_mixture_properties(self, mixture: Dict[str, float]) -> np.ndarray:
        """Calculate properties using rule of mixtures."""
        props = np.zeros(3)  # tensile, modulus, density
        
        for fiber, ratio in mixture.items():
            if fiber in self.fiber_properties:
                fiber_props = self.fiber_properties[fiber]
                props[0] += ratio * fiber_props['tensile']
                props[1] += ratio * fiber_props['modulus']
                props[2] += ratio * fiber_props['density']
                
        return props
    
    def __len__(self) -> int:
        return len(self.mixtures)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        # Encode mixture as feature vector
        features = np.zeros(len(self.base_fibers))
        
        for fiber, ratio in self.mixtures[idx].items():
            if fiber in self.base_fibers:
                fiber_idx = self.base_fibers.index(fiber)
                features[fiber_idx] = ratio
                
        return {
            'features': torch.FloatTensor(features),
            'properties': torch.FloatTensor(self.properties[idx]),
            'mixture': self.mixtures[idx]
        }


def create_dataloaders(data_path: str,
                      batch_size: int = 32,
                      num_workers: int = 4,
                      target_properties: Optional[List[str]] = None) -> Dict[str, DataLoader]:
    """
    Create data loaders for train, validation, and test sets.
    
    Args:
        data_path: Path to data directory
        batch_size: Batch size for training
        num_workers: Number of worker processes
        target_properties: List of properties to predict
        
    Returns:
        Dictionary of DataLoaders
    """
    dataloaders = {}
    
    for mode in ['train', 'val', 'test']:
        dataset = FiberPolymerDataset(
            data_path=data_path,
            mode=mode,
            target_properties=target_properties,
            augment=(mode == 'train')
        )
        
        dataloaders[mode] = DataLoader(
            dataset,
            batch_size=batch_size if mode == 'train' else batch_size * 2,
            shuffle=(mode == 'train'),
            num_workers=num_workers,
            pin_memory=True
        )
        
    return dataloaders 