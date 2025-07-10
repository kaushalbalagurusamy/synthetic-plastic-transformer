# Python Development Patterns

## Type Annotations
All functions, methods, and class members MUST have type annotations:

```python
from typing import Optional, List, Dict, Any, Union, Tuple, Generator
from pydantic import BaseModel, Field

async def predict_replacement(
    target_properties: Dict[str, float],
    constraints: Optional[Dict[str, Any]] = None
) -> List[FiberRecommendation]:
    """Predict natural fiber replacements for target properties.
    
    Args:
        target_properties: Dictionary of desired material properties.
        constraints: Optional constraints for the prediction.
        
    Returns:
        List of fiber recommendations sorted by match score.
        
    Raises:
        ValueError: If target_properties are invalid.
    """
    pass
```

## Error Handling
Define domain-specific exceptions:

```python
class ChemistryError(Exception):
    """Base exception for chemistry-related errors."""
    pass

class InvalidMoleculeError(ChemistryError):
    """Raised when molecule structure is invalid."""
    pass

class GOTSComplianceError(ChemistryError):
    """Raised when GOTS standards are violated."""
    def __init__(self, violation: str, blend: Dict[str, float]) -> None:
        self.violation = violation
        self.blend = blend
        super().__init__(f"GOTS violation: {violation} for blend {blend}")
```

## Resource Management
Use context managers:

```python
from contextlib import contextmanager
import gc

@contextmanager
def gpu_memory_manager() -> Generator[None, None, None]:
    """Manage GPU memory for large models."""
    try:
        torch.cuda.empty_cache()
        yield
    finally:
        torch.cuda.empty_cache()
        gc.collect()
```

## Data Processing
Use generators for large datasets:

```python
def process_molecules_batch(
    smiles_list: List[str],
    batch_size: int = 1000
) -> Generator[List[Chem.Mol], None, None]:
    """Process molecules in batches to manage memory."""
    for i in range(0, len(smiles_list), batch_size):
        batch = smiles_list[i:i + batch_size]
        molecules = [Chem.MolFromSmiles(s) for s in batch]
        yield [m for m in molecules if m is not None]
```

## Async Patterns
Use async/await for I/O operations:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def fetch_polymer_data(
    polymer_id: str,
    db: AsyncSession
) -> Optional[PolymerProperties]:
    """Fetch polymer data from database asynchronously.
    
    Args:
        polymer_id: Unique identifier for the polymer.
        db: Async database session.
        
    Returns:
        Polymer properties if found, None otherwise.
    """
    async with db.begin():
        result = await db.execute(
            select(PolymerProperties).where(
                PolymerProperties.id == polymer_id
            )
        )
        return result.scalar_one_or_none()
```

## Logging
Use structured logging:

```python
from loguru import logger

logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    format="{time} {level} {message}",
    level="INFO"
)

# Usage
logger.info("Processing molecule", smiles=smiles, properties=props)
logger.error("Failed to process", error=str(e), molecule_id=mol_id)