"""
Unit tests for quantum descriptor calculations.
"""

import pytest
import torch
import numpy as np
from rdkit import Chem
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from models.quantum_descriptors import (
    QuantumDescriptorCalculator,
    QuantumInformedFeatures
)


class TestQuantumDescriptorCalculator:
    """Test quantum descriptor calculations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = QuantumDescriptorCalculator(use_ml_predictions=False)
        
    def test_basic_descriptors(self):
        """Test basic molecular descriptor calculation."""
        # Test with a simple molecule (ethanol)
        mol = Chem.MolFromSmiles('CCO')
        descriptors = self.calculator.calculate_descriptors(mol)
        
        # Check that all basic descriptors are present
        assert 'molecular_weight' in descriptors
        assert 'logp' in descriptors
        assert 'tpsa' in descriptors
        assert 'num_rotatable_bonds' in descriptors
        
        # Check specific values for ethanol
        assert 44 < descriptors['molecular_weight'] < 47
        assert descriptors['num_h_donors'] == 1
        assert descriptors['num_h_acceptors'] == 1
        
    def test_electronic_descriptors(self):
        """Test electronic descriptor calculation."""
        # Test with benzene
        mol = Chem.MolFromSmiles('c1ccccc1')
        descriptors = self.calculator.calculate_descriptors(mol)
        
        # Check electronic descriptors
        assert 'max_partial_charge' in descriptors
        assert 'min_partial_charge' in descriptors
        assert 'molar_refractivity' in descriptors
        
        # Benzene should have relatively uniform charges
        assert abs(descriptors['max_partial_charge'] - descriptors['min_partial_charge']) < 0.2
        
    def test_topological_descriptors(self):
        """Test topological descriptor calculation."""
        # Test with a branched molecule
        mol = Chem.MolFromSmiles('CC(C)CC')
        descriptors = self.calculator.calculate_descriptors(mol)
        
        # Check topological indices
        assert 'chi0' in descriptors
        assert 'chi1' in descriptors
        assert 'kappa1' in descriptors
        assert 'hall_kier_alpha' in descriptors
        
        # All should be positive for this molecule
        assert descriptors['chi0'] > 0
        assert descriptors['chi1'] > 0
        
    def test_quantum_estimates(self):
        """Test quantum mechanical descriptor estimates."""
        # Test with conjugated molecule (butadiene)
        mol = Chem.MolFromSmiles('C=CC=C')
        descriptors = self.calculator.calculate_descriptors(mol)
        
        # Check quantum descriptors
        assert 'homo_lumo_gap_est' in descriptors
        assert 'dipole_moment_est' in descriptors
        assert 'polarizability_est' in descriptors
        
        # Conjugated system should have lower HOMO-LUMO gap
        assert 1.0 < descriptors['homo_lumo_gap_est'] < 8.0
        
        # Test aromatic molecule
        mol_aromatic = Chem.MolFromSmiles('c1ccc(cc1)c2ccccc2')  # Biphenyl
        desc_aromatic = self.calculator.calculate_descriptors(mol_aromatic)
        
        # More aromatic rings should lower the gap
        assert desc_aromatic['homo_lumo_gap_est'] < descriptors['homo_lumo_gap_est']
        
    def test_polymer_descriptors(self):
        """Test descriptors for polymer-like molecules."""
        # Test with PET repeat unit
        mol = Chem.MolFromSmiles('O=C(O)c1ccc(cc1)C(=O)OCC')
        descriptors = self.calculator.calculate_descriptors(mol)
        
        # Should have reasonable values
        assert descriptors['molecular_weight'] > 100
        assert descriptors['num_aromatic_rings'] == 1
        assert descriptors['num_rotatable_bonds'] > 3
        
    def test_invalid_smiles(self):
        """Test handling of invalid SMILES."""
        with pytest.raises(ValueError):
            self.calculator.calculate_descriptors('invalid_smiles')
            
    def test_conjugation_estimation(self):
        """Test conjugation score estimation."""
        # Linear conjugated system
        mol1 = Chem.MolFromSmiles('C=CC=CC=C')
        conj1 = self.calculator._estimate_conjugation(mol1)
        
        # Aromatic system
        mol2 = Chem.MolFromSmiles('c1ccccc1')
        conj2 = self.calculator._estimate_conjugation(mol2)
        
        # Both should have significant conjugation
        assert conj1 > 2
        assert conj2 > 4  # Aromatic bonds count more


class TestQuantumInformedFeatures:
    """Test quantum-informed neural network features."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.module = QuantumInformedFeatures(
            num_base_features=10,
            num_quantum_features=17,
            hidden_dim=64
        )
        
    def test_forward_pass(self):
        """Test forward pass through the module."""
        batch_size = 4
        base_features = torch.randn(batch_size, 10)
        quantum_features = torch.randn(batch_size, 17)
        
        output = self.module(base_features, quantum_features)
        
        # Check output shape
        assert output.shape == (batch_size, 64)
        
        # Check that output is not NaN
        assert not torch.isnan(output).any()
        
    def test_batch_feature_extraction(self):
        """Test batch extraction of quantum features."""
        smiles_list = [
            'CCO',  # Ethanol
            'c1ccccc1',  # Benzene
            'CC(=O)O',  # Acetic acid
            'CCCCCCCC'  # Octane
        ]
        
        features = self.module.extract_quantum_features_batch(smiles_list)
        
        # Check shape
        assert features.shape == (4, 17)  # 4 molecules, 17 features
        
        # Check that features are different for different molecules
        assert not torch.allclose(features[0], features[1])
        
        # Check specific feature differences
        # Benzene should have different aromaticity than others
        benzene_idx = 1
        assert features[benzene_idx, 6] > 0  # num_aromatic_rings position
        
    def test_invalid_smiles_handling(self):
        """Test handling of invalid SMILES in batch."""
        smiles_list = [
            'CCO',
            'invalid_smiles',
            'c1ccccc1'
        ]
        
        features = self.module.extract_quantum_features_batch(smiles_list)
        
        # Should still return correct shape
        assert features.shape == (3, 17)
        
        # Invalid SMILES should give zero features
        assert torch.all(features[1] == 0)
        
        # Valid molecules should still have features
        assert torch.any(features[0] != 0)
        assert torch.any(features[2] != 0)


def test_descriptor_ranges():
    """Test that descriptors are in reasonable ranges."""
    calculator = QuantumDescriptorCalculator(use_ml_predictions=False)
    
    # Test various molecules
    test_molecules = [
        'CC',  # Ethane
        'c1ccccc1',  # Benzene
        'O=C(O)CCCCC(=O)O',  # Adipic acid
        'CC(C)(C)C',  # tert-Butane
        'c1ccc2c(c1)ccc1c2cccc1'  # Anthracene
    ]
    
    for smiles in test_molecules:
        mol = Chem.MolFromSmiles(smiles)
        descriptors = calculator.calculate_descriptors(mol)
        
        # Check reasonable ranges
        assert 0 < descriptors['molecular_weight'] < 1000
        assert -10 < descriptors['logp'] < 10
        assert 0 <= descriptors['tpsa'] < 200
        assert 0 <= descriptors['fraction_csp3'] <= 1
        assert 1 <= descriptors['homo_lumo_gap_est'] <= 12
        assert 0 <= descriptors['dipole_moment_est'] < 20
        assert descriptors['polarizability_est'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 