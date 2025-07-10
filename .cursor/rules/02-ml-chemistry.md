# ML/Chemistry Development Guidelines

## Chemical Data Validation
Always validate chemical structures:

```python
from rdkit import Chem
from typing import Optional
import numpy as np

def process_molecule(smiles: str) -> Optional[Chem.Mol]:
    """Process SMILES string to RDKit molecule with validation."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")
        
        # Additional validation
        if mol.GetNumAtoms() == 0:
            raise ValueError("Molecule has no atoms")
        if mol.GetNumAtoms() > 500:
            raise ValueError("Molecule too large for processing")
            
        return mol
    except Exception as e:
        logger.error(f"Failed to process molecule: {e}")
        return None
```

## Reproducibility
Set random seeds for all libraries:

```python
import random
import numpy as np
import torch

def set_reproducibility(seed: int = 42) -> None:
    """Set random seeds for all libraries."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    # Set environment variable for transformers
    import os
    os.environ["PYTHONHASHSEED"] = str(seed)
```

## Model Development
Structure for neural networks:

```python
from typing import Dict, Tuple
import torch
import torch.nn as nn
from abc import ABC, abstractmethod

class BaseModel(nn.Module, ABC):
    """Base class for all models in the project."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__()
        self.config = config
        self._build_model()
    
    @abstractmethod
    def _build_model(self) -> None:
        """Build the model architecture."""
        pass
    
    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        pass
    
    def get_num_params(self) -> int:
        """Get total number of parameters."""
        return sum(p.numel() for p in self.parameters())
```

## Quantum Descriptors
Calculate molecular properties:

```python
from rdkit.Chem import Descriptors, Crippen
from mordred import Calculator, descriptors

def calculate_quantum_descriptors(molecule: Chem.Mol) -> Dict[str, float]:
    """Calculate quantum mechanical descriptors for a molecule.
    
    Args:
        molecule: RDKit molecule object.
        
    Returns:
        Dictionary of quantum descriptors.
    """
    # Basic descriptors
    descriptors_dict = {
        "molecular_weight": Descriptors.MolWt(molecule),
        "logp": Crippen.MolLogP(molecule),
        "tpsa": Descriptors.TPSA(molecule),
        "num_rotatable_bonds": Descriptors.NumRotatableBonds(molecule),
        "num_h_donors": Descriptors.NumHDonors(molecule),
        "num_h_acceptors": Descriptors.NumHAcceptors(molecule),
    }
    
    # Mordred descriptors for more complex properties
    calc = Calculator(descriptors, ignore_3D=True)
    mordred_desc = calc(molecule)
    
    # Add selected Mordred descriptors
    descriptors_dict.update({
        f"mordred_{key}": float(value) 
        for key, value in mordred_desc.items() 
        if not isinstance(value, str) and np.isfinite(float(value))
    })
    
    return descriptors_dict
```

## Batch Processing
Efficient batch processing for ML:

```python
from torch.utils.data import DataLoader, Dataset
from typing import List, Tuple

class MoleculeDataset(Dataset):
    """Dataset for molecular property prediction."""
    
    def __init__(
        self, 
        smiles_list: List[str], 
        properties: Optional[np.ndarray] = None,
        transform: Optional[Callable] = None
    ) -> None:
        self.smiles_list = smiles_list
        self.properties = properties
        self.transform = transform
        
    def __len__(self) -> int:
        return len(self.smiles_list)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        smiles = self.smiles_list[idx]
        mol = Chem.MolFromSmiles(smiles)
        
        # Convert to features
        features = self.mol_to_features(mol)
        if self.transform:
            features = self.transform(features)
            
        if self.properties is not None:
            return features, torch.tensor(self.properties[idx])
        return features, None
```

## Model Evaluation
Comprehensive evaluation metrics:

```python
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from typing import Dict, Tuple

def evaluate_regression_model(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    property_name: str
) -> Dict[str, float]:
    """Evaluate regression model performance.
    
    Args:
        y_true: True values.
        y_pred: Predicted values.
        property_name: Name of the property being predicted.
        
    Returns:
        Dictionary of evaluation metrics.
    """
    metrics = {
        f"{property_name}_rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        f"{property_name}_mae": mean_absolute_error(y_true, y_pred),
        f"{property_name}_r2": r2_score(y_true, y_pred),
        f"{property_name}_mape": np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    }
    
    # Add percentile errors
    errors = np.abs(y_true - y_pred)
    metrics.update({
        f"{property_name}_p50_error": np.percentile(errors, 50),
        f"{property_name}_p90_error": np.percentile(errors, 90),
        f"{property_name}_p95_error": np.percentile(errors, 95),
    })
    
    return metrics
```