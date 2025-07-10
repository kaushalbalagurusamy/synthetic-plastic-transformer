# Model Training Commands

## Train Models

### Train with Quantum Descriptors
```bash
# Train a new model with quantum descriptors
spt-train --config configs/quantum_transfer.yaml --use-gpu

# Train with specific hyperparameters
spt-train \
  --config configs/base_config.yaml \
  --learning-rate 1e-4 \
  --batch-size 32 \
  --epochs 100 \
  --use-quantum-descriptors \
  --use-gpu
```

### Transfer Learning
```bash
# Fine-tune from QM9 pretrained model
python train.py --config configs/transfer_config.yaml \
                --pretrained_model models/schnet_qm9.pth \
                --freeze_encoder_epochs 5

# Fine-tune from protein folding model
python -m src.transfer_learning.protein_transfer \
  --base-model models/alphafold_base.pth \
  --target-dataset polymer_properties \
  --output-dir models/protein_transfer/
```

### Multi-Task Training
```bash
# Train on all properties simultaneously
python train.py --config configs/multitask_config.yaml \
                --loss_weights tensile:1.0 modulus:1.0 biodegradability:1.5

# Train with custom property weights
python -m src.training.multitask_trainer \
  --properties tensile_strength elastic_modulus density \
  --weights 1.0 0.8 0.5 \
  --validate-every 10
```

### Self-Supervised Pretraining
```bash
# Pretrain on unlabeled polymer structures
python pretrain.py --config configs/self_supervised_config.yaml \
                   --dataset PI1M \
                   --tasks masked_atom contrastive

# Pretrain with specific SSL methods
python -m src.models.self_supervised_learning \
  --method masked_atom_prediction \
  --mask-ratio 0.15 \
  --dataset-path data/unlabeled_polymers/ \
  --epochs 50
```

## Model Evaluation

### Evaluate Trained Models
```bash
# Evaluate model on test set
spt-evaluate --model-path models/best_model.pth --test-split 0.2

# Evaluate with specific metrics
spt-evaluate \
  --model-path models/quantum_model.pth \
  --metrics rmse mae r2 mape \
  --save-predictions results/predictions.csv
```

### Cross-Validation
```bash
# Run k-fold cross-validation
python -m src.evaluation.cross_validate \
  --model-config configs/base_config.yaml \
  --n-folds 5 \
  --stratify-by scaffold
```

### Generate Predictions
```bash
# Generate predictions for specific polymer
spt-predict --smiles "CC(C)CC(C)CC(C)C" --output results/hdpe_alternatives.json

# Batch predictions
spt-predict \
  --input-file data/test_polymers.csv \
  --output-dir results/batch_predictions/ \
  --batch-size 100
```

## Hyperparameter Optimization

### Optuna Optimization
```bash
# Run hyperparameter optimization
python -m src.optimization.optuna_search \
  --config configs/optuna_config.yaml \
  --n-trials 100 \
  --study-name polymer_optimization

# Resume optimization
python -m src.optimization.optuna_search \
  --resume-study polymer_optimization \
  --n-trials 50
```

### Grid Search
```bash
# Run grid search
python -m src.optimization.grid_search \
  --param-grid configs/param_grid.yaml \
  --cv-folds 3 \
  --n-jobs -1
```

## Model Management

### Save and Load Models
```bash
# Save model checkpoint
python -m src.utils.model_utils save \
  --model-path models/current_model.pth \
  --save-path models/checkpoints/model_epoch_50.pth \
  --include-optimizer

# Load and convert model
python -m src.utils.model_utils convert \
  --input-path models/pytorch_model.pth \
  --output-format onnx \
  --output-path models/exported/model.onnx
```

### Model Versioning
```bash
# Register model version
python -m src.utils.model_registry register \
  --model-path models/best_model.pth \
  --version 1.2.0 \
  --metrics-file results/evaluation_metrics.json \
  --description "Quantum descriptors + transfer learning"

# Compare model versions
python -m src.utils.model_registry compare \
  --version1 1.1.0 \
  --version2 1.2.0 \
  --test-data data/test_set.pkl
```

## Training Monitoring

### TensorBoard
```bash
# Start TensorBoard
tensorboard --logdir runs/ --port 6006

# Start with specific run
tensorboard --logdir runs/quantum_transfer_2024/ --port 6006
```

### MLflow Tracking
```bash
# Start MLflow UI
mlflow ui --host 0.0.0.0 --port 5000

# Track experiment
python train.py --config configs/base.yaml --mlflow-experiment polymer_prediction
```

## Distributed Training

### Multi-GPU Training
```bash
# Train on multiple GPUs
python -m torch.distributed.launch \
  --nproc_per_node=4 \
  train.py --config configs/distributed.yaml

# Specific GPU selection
CUDA_VISIBLE_DEVICES=0,1,2,3 python train.py \
  --config configs/base.yaml \
  --distributed \
  --backend nccl
```

### Cloud Training
```bash
# Submit training job to cloud
python -m src.cloud.submit_job \
  --config configs/cloud_training.yaml \
  --instance-type p3.8xlarge \
  --spot-instances \
  --max-runtime 12h
```