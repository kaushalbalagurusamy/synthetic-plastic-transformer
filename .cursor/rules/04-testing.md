# Testing Guidelines

## Test Structure
Use pytest with proper organization:

```python
from typing import TYPE_CHECKING
import pytest
from unittest.mock import Mock, AsyncMock, patch
import asyncio

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture
```

## Fixtures
Create reusable test fixtures:

```python
# conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, class_=AsyncSession)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()

@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide test client with database override."""
    def override_get_db():
        return test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def mock_model(mocker: MockerFixture) -> Mock:
    """Mock ML model for testing."""
    mock = mocker.Mock()
    mock.predict.return_value = {
        "tensile_strength": 500.0,
        "elastic_modulus": 10.0
    }
    mock.model_version = "1.0.0"
    return mock
```

## Unit Tests
Test individual components:

```python
import pytest
from src.models.quantum_descriptors import calculate_quantum_descriptors
from rdkit import Chem

class TestQuantumDescriptors:
    """Test quantum descriptor calculations."""
    
    @pytest.mark.parametrize("smiles,expected_mw", [
        ("CCO", 46.07),
        ("CC(C)C", 58.12),
        ("c1ccccc1", 78.11),
    ])
    def test_molecular_weight(
        self, 
        smiles: str, 
        expected_mw: float
    ) -> None:
        """Test molecular weight calculation."""
        mol = Chem.MolFromSmiles(smiles)
        descriptors = calculate_quantum_descriptors(mol)
        
        assert "molecular_weight" in descriptors
        assert pytest.approx(descriptors["molecular_weight"], rel=0.01) == expected_mw
    
    def test_invalid_molecule(self) -> None:
        """Test handling of invalid molecules."""
        with pytest.raises(ValueError, match="Invalid SMILES"):
            mol = Chem.MolFromSmiles("invalid")
            calculate_quantum_descriptors(mol)
    
    @pytest.fixture
    def sample_molecule(self) -> Chem.Mol:
        """Provide sample molecule for testing."""
        return Chem.MolFromSmiles("CC(=O)O")  # Acetic acid
    
    def test_descriptor_completeness(
        self, 
        sample_molecule: Chem.Mol
    ) -> None:
        """Test that all expected descriptors are calculated."""
        descriptors = calculate_quantum_descriptors(sample_molecule)
        
        expected_keys = {
            "molecular_weight",
            "logp",
            "tpsa",
            "num_rotatable_bonds",
            "num_h_donors",
            "num_h_acceptors"
        }
        
        assert expected_keys.issubset(descriptors.keys())
        assert all(isinstance(v, (int, float)) for v in descriptors.values())
```

## Async Tests
Test async functions properly:

```python
@pytest.mark.asyncio
async def test_predict_endpoint(
    client: AsyncClient,
    mock_model: Mock,
    mocker: MockerFixture
) -> None:
    """Test prediction endpoint."""
    # Mock the ML service
    mocker.patch("src.api.routes.get_ml_service", return_value=mock_model)
    
    # Prepare request
    request_data = {
        "target_properties": {
            "tensile_strength": 500.0,
            "elastic_modulus": 10.0
        },
        "max_results": 5
    }
    
    # Make request
    response = await client.post(
        "/api/v1/predict",
        json=request_data,
        headers={"Authorization": "Bearer test-token"}
    )
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) <= 5
    assert "processing_time" in data
    assert data["model_version"] == "1.0.0"

@pytest.mark.asyncio
async def test_database_operations(
    test_db: AsyncSession
) -> None:
    """Test database operations."""
    # Create test data
    fiber = FiberProperties(
        name="test_hemp",
        tensile_strength_min=300.0,
        tensile_strength_max=900.0,
        elastic_modulus=70.0
    )
    
    test_db.add(fiber)
    await test_db.commit()
    
    # Query data
    result = await test_db.execute(
        select(FiberProperties).where(FiberProperties.name == "test_hemp")
    )
    retrieved = result.scalar_one()
    
    assert retrieved.name == "test_hemp"
    assert retrieved.elastic_modulus == 70.0
```

## Integration Tests
Test complete workflows:

```python
@pytest.mark.integration
class TestPredictionWorkflow:
    """Test complete prediction workflow."""
    
    @pytest.mark.asyncio
    async def test_full_prediction_workflow(
        self,
        client: AsyncClient,
        test_db: AsyncSession
    ) -> None:
        """Test complete prediction from request to response."""
        # Setup: Create test user
        user = await create_test_user(test_db)
        token = generate_test_token(user)
        
        # Setup: Load test model
        await load_test_model()
        
        # Execute prediction
        response = await client.post(
            "/api/v1/predict",
            json={
                "target_properties": {
                    "tensile_strength": 600.0,
                    "elastic_modulus": 15.0,
                    "density": 1.2
                },
                "constraints": {
                    "require_organic": True,
                    "max_cost": 150.0
                }
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert all(key in data for key in ["recommendations", "processing_time", "model_version"])
        
        # Validate recommendations
        for rec in data["recommendations"]:
            assert rec["gots_compliant"] is True
            assert sum(rec["fiber_composition"].values()) == pytest.approx(100.0, rel=0.01)
            assert 0.0 <= rec["match_score"] <= 1.0
```

## Performance Tests
Test performance requirements:

```python
@pytest.mark.performance
def test_descriptor_calculation_performance(
    benchmark,
    sample_molecules: List[Chem.Mol]
) -> None:
    """Test descriptor calculation performance."""
    def calculate_all():
        return [calculate_quantum_descriptors(mol) for mol in sample_molecules]
    
    result = benchmark(calculate_all)
    
    # Assert performance requirements
    assert benchmark.stats["mean"] < 0.1  # Average < 100ms
    assert benchmark.stats["max"] < 0.5   # Max < 500ms

@pytest.mark.asyncio
@pytest.mark.timeout(5)  # 5 second timeout
async def test_api_response_time(client: AsyncClient) -> None:
    """Test API response time."""
    import time
    
    start = time.time()
    response = await client.get("/api/v1/health")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 0.1  # Response within 100ms
```

## Test Coverage
Ensure comprehensive coverage:

```bash
# pytest.ini configuration
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=90"
]
testpaths = ["tests"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "performance: Performance tests",
    "asyncio: Async tests"
]
```