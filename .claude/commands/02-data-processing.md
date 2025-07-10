# Data Processing Commands

## Fiber Data Management

### Process New Fiber Data
```bash
# Process new fiber data from CSV
python -m src.preprocessing.process_fibers --input data/raw/new_fibers.csv

# Process with validation
python -m src.preprocessing.process_fibers \
  --input data/raw/new_fibers.csv \
  --validate-gots \
  --output data/processed/validated_fibers.json
```

### Update Fiber Database
```bash
# Add new fiber to database
python -m src.data.fiber_manager add \
  --name "banana_fiber" \
  --tensile-strength-min 500 \
  --tensile-strength-max 750 \
  --elastic-modulus 12.0 \
  --density 1.35

# Import batch of fibers
python -m src.data.fiber_manager import \
  --file data/new_fibers.json \
  --validate \
  --update-existing
```

## Molecular Descriptors

### Generate Descriptors
```bash
# Generate molecular descriptors for dataset
python -m src.models.quantum_descriptors --dataset polymer_db --output descriptors.pkl

# Generate specific descriptor types
python -m src.models.quantum_descriptors \
  --input data/molecules.sdf \
  --descriptor-types mordred rdkit quantum \
  --output data/processed/all_descriptors.pkl
```

### Calculate Quantum Properties
```bash
# Calculate HOMO-LUMO gaps
python -m src.quantum.calculate_properties \
  --smiles-file data/polymers.smi \
  --properties homo_lumo_gap partial_charges \
  --method PM7 \
  --output quantum_properties.csv
```

## GOTS Compliance Validation

### Validate Fiber Blends
```bash
# Validate GOTS compliance for fiber blend
python -m src.utils.gots_compliance --blend "hemp:45,flax:30,silk:25"

# Batch validation
python -m src.utils.gots_compliance \
  --blend-file data/test_blends.csv \
  --output validation_results.json \
  --strict-mode
```

### Check Processing Methods
```bash
# Validate processing parameters
python -m src.utils.gots_compliance check_processing \
  --temperature 120 \
  --chemicals "citric_acid,hydrogen_peroxide" \
  --fiber-type hemp
```

## Data Preprocessing

### Polymer Data Processing
```bash
# Process polymer SMILES strings
python -m src.preprocessing.polymer_processor \
  --input data/raw/polymers.csv \
  --validate-smiles \
  --calculate-descriptors \
  --output data/processed/polymers_processed.pkl

# Clean and standardize molecules
python -m src.preprocessing.molecule_cleaner \
  --input data/raw/molecules.sdf \
  --remove-salts \
  --neutralize \
  --canonical-smiles \
  --output data/clean/molecules_clean.sdf
```

### Feature Engineering
```bash
# Generate features for ML
python -m src.preprocessing.feature_engineering \
  --molecule-file data/processed/molecules.pkl \
  --feature-types fingerprints descriptors graph \
  --output data/features/

# Create custom features
python -m src.preprocessing.custom_features \
  --config configs/feature_config.yaml \
  --input data/processed/ \
  --output data/features/custom/
```

## Dataset Creation

### Create Training Datasets
```bash
# Create ML-ready dataset
python -m src.data.create_dataset \
  --molecules data/processed/polymers.pkl \
  --properties data/raw/properties.csv \
  --split-method scaffold \
  --test-size 0.2 \
  --val-size 0.1 \
  --output data/ml_datasets/

# Create dataset with augmentation
python -m src.data.create_dataset \
  --molecules data/processed/polymers.pkl \
  --augment-smiles \
  --augment-factor 5 \
  --balance-properties \
  --output data/ml_datasets/augmented/
```

### Data Validation
```bash
# Validate dataset integrity
python -m src.data.validate_dataset \
  --dataset data/ml_datasets/train.pkl \
  --check-duplicates \
  --check-distribution \
  --check-properties-range

# Check data quality
python -m src.data.quality_check \
  --dataset data/ml_datasets/ \
  --report-output reports/data_quality.html
```

## Data Transformation

### Convert Formats
```bash
# Convert between molecular formats
python -m src.utils.format_converter \
  --input data/molecules.smi \
  --input-format smiles \
  --output data/molecules.sdf \
  --output-format sdf

# Convert to graph format
python -m src.data.to_graph \
  --molecules data/processed/molecules.pkl \
  --output data/graphs/ \
  --include-3d-coords
```

### Batch Processing
```bash
# Process large dataset in batches
python -m src.preprocessing.batch_processor \
  --input data/large_dataset.csv \
  --batch-size 10000 \
  --n-workers 8 \
  --task calculate_descriptors \
  --output data/processed/batches/
```

## Data Analysis

### Exploratory Data Analysis
```bash
# Generate EDA report
python -m src.analysis.eda \
  --dataset data/ml_datasets/train.pkl \
  --output reports/eda_report.html \
  --include-correlations \
  --include-distributions

# Analyze property distributions
python -m src.analysis.property_analysis \
  --dataset data/processed/polymers.pkl \
  --properties tensile_strength elastic_modulus \
  --plot-output figures/property_distributions/
```

### Statistical Analysis
```bash
# Compare fiber properties
python -m src.analysis.compare_fibers \
  --fiber1 hemp \
  --fiber2 flax \
  --properties all \
  --statistical-test mann-whitney

# Correlation analysis
python -m src.analysis.correlations \
  --dataset data/ml_datasets/train.pkl \
  --method spearman \
  --threshold 0.7 \
  --output reports/high_correlations.csv
```

## Database Operations

### Initialize Database
```bash
# Initialize database schema
python -m src.database.init_db

# Initialize with sample data
python -m src.database.init_db --with-samples

# Reset database
python -m src.database.init_db --reset --confirm
```

### Data Import/Export
```bash
# Import data to database
python -m src.database.import_data \
  --table polymers \
  --file data/polymers.csv \
  --update-existing

# Export database to file
python -m src.database.export_data \
  --table fiber_properties \
  --format json \
  --output backups/fibers_backup.json
```

### Database Maintenance
```bash
# Backup database
pg_dump -U postgres spt_db > backup_$(date +%Y%m%d).sql

# Vacuum and analyze
python -m src.database.maintenance vacuum analyze

# Check integrity
python -m src.database.maintenance check_integrity
```