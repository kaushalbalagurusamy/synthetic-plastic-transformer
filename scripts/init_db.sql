-- Database initialization script for Synthetic Plastic Transformer
-- This script sets up the initial database schema

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schema for the application
CREATE SCHEMA IF NOT EXISTS spt;

-- Set search path
SET search_path TO spt, public;

-- Table for storing natural fiber properties
CREATE TABLE IF NOT EXISTS natural_fibers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL, -- bast, leaf, seed, protein, etc.
    tensile_strength_min DECIMAL(10,2),
    tensile_strength_max DECIMAL(10,2),
    elastic_modulus_min DECIMAL(10,2),
    elastic_modulus_max DECIMAL(10,2),
    density DECIMAL(8,3),
    water_absorption DECIMAL(5,2),
    thermal_conductivity DECIMAL(8,4),
    uv_resistance DECIMAL(3,2),
    biodegradability_rate DECIMAL(5,2),
    gots_compliant BOOLEAN DEFAULT false,
    processing_temp_max INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing polymer data
CREATE TABLE IF NOT EXISTS polymers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    smiles TEXT,
    molecular_weight DECIMAL(12,3),
    glass_transition_temp DECIMAL(8,2),
    melting_point DECIMAL(8,2),
    tensile_strength DECIMAL(10,2),
    elastic_modulus DECIMAL(10,2),
    thermal_conductivity DECIMAL(8,4),
    density DECIMAL(8,3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing experimental results
CREATE TABLE IF NOT EXISTS experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_name VARCHAR(200) NOT NULL,
    target_properties JSONB NOT NULL,
    fiber_composition JSONB NOT NULL,
    predicted_properties JSONB,
    actual_properties JSONB,
    processing_method VARCHAR(100),
    processing_parameters JSONB,
    gots_compliant BOOLEAN,
    property_match_score DECIMAL(5,4),
    model_version VARCHAR(50),
    experiment_date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing model metadata
CREATE TABLE IF NOT EXISTS models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    architecture VARCHAR(100),
    training_dataset VARCHAR(100),
    performance_metrics JSONB,
    model_path VARCHAR(500),
    is_active BOOLEAN DEFAULT false,
    trained_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

-- Table for storing prediction requests and results
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100),
    target_properties JSONB NOT NULL,
    constraints JSONB,
    recommendations JSONB,
    model_id UUID REFERENCES models(id),
    processing_time_ms INTEGER,
    confidence_score DECIMAL(5,4),
    request_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Table for storing GOTS compliance rules
CREATE TABLE IF NOT EXISTS gots_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_type VARCHAR(50) NOT NULL, -- fiber, processing, chemical, etc.
    rule_name VARCHAR(100) NOT NULL,
    rule_description TEXT,
    allowed_values JSONB,
    max_percentage DECIMAL(5,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial natural fiber data
INSERT INTO natural_fibers (name, category, tensile_strength_min, tensile_strength_max, 
                           elastic_modulus_min, elastic_modulus_max, density, water_absorption,
                           gots_compliant, processing_temp_max) VALUES
('Hemp', 'bast', 550, 1110, 3.7, 90, 1.48, 8.0, true, 200),
('Flax', 'bast', 345, 1500, 27.6, 80, 1.54, 7.0, true, 180),
('Cotton', 'seed', 287, 800, 5.5, 12.6, 1.52, 8.5, true, 150),
('Jute', 'bast', 393, 800, 13, 26.5, 1.46, 12.0, true, 160),
('Ramie', 'bast', 400, 938, 61.4, 128, 1.55, 6.2, true, 170),
('Sisal', 'leaf', 468, 700, 9.4, 22, 1.45, 11.0, true, 140),
('Pineapple', 'leaf', 413, 1627, 1.44, 82.51, 1.44, 13.2, true, 120),
('Coir', 'seed', 131, 220, 4, 6, 1.15, 10.0, true, 100),
('Banana', 'leaf', 529, 914, 7.7, 20, 1.35, 9.5, true, 110),
('Bamboo', 'grass', 140, 800, 11, 32, 1.2, 8.9, true, 130),
('Silk', 'protein', 300, 740, 5, 25, 1.34, 11.0, true, 160),
('Wool', 'protein', 50, 320, 2, 5.5, 1.31, 13.6, true, 120),
('Kapok', 'seed', 89, 159, 0.2, 0.89, 0.35, 0.4, true, 80),
('Kenaf', 'bast', 240, 600, 14.5, 53, 1.2, 21.5, true, 150);

-- Insert GOTS compliance rules
INSERT INTO gots_rules (rule_type, rule_name, rule_description, allowed_values, is_active) VALUES
('fiber', 'organic_content', 'Minimum organic fiber content required', '{"min_percentage": 70}', true),
('processing', 'chemical_treatments', 'Allowed chemical treatments', 
 '{"allowed": ["enzymatic", "citric_acid", "hydrogen_peroxide_low"], "forbidden": ["formaldehyde", "heavy_metals"]}', true),
('processing', 'temperature_limits', 'Maximum processing temperatures', '{"max_temp_celsius": 200}', true),
('environmental', 'water_treatment', 'Water treatment requirements', 
 '{"required": true, "treatment_efficiency": 90}', true);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_natural_fibers_gots ON natural_fibers(gots_compliant);
CREATE INDEX IF NOT EXISTS idx_natural_fibers_category ON natural_fibers(category);
CREATE INDEX IF NOT EXISTS idx_experiments_date ON experiments(experiment_date);
CREATE INDEX IF NOT EXISTS idx_experiments_model_version ON experiments(model_version);
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON predictions(request_timestamp);
CREATE INDEX IF NOT EXISTS idx_predictions_model_id ON predictions(model_id);
CREATE INDEX IF NOT EXISTS idx_models_active ON models(is_active);

-- Create function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_natural_fibers_updated_at BEFORE UPDATE ON natural_fibers 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_polymers_updated_at BEFORE UPDATE ON polymers 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_experiments_updated_at BEFORE UPDATE ON experiments 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_models_updated_at BEFORE UPDATE ON models 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gots_rules_updated_at BEFORE UPDATE ON gots_rules 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed for your environment)
GRANT USAGE ON SCHEMA spt TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA spt TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA spt TO postgres;

-- Create a view for commonly queried fiber properties
CREATE OR REPLACE VIEW fiber_properties_summary AS
SELECT 
    name,
    category,
    (tensile_strength_min + tensile_strength_max) / 2 AS avg_tensile_strength,
    (elastic_modulus_min + elastic_modulus_max) / 2 AS avg_elastic_modulus,
    density,
    water_absorption,
    gots_compliant,
    processing_temp_max
FROM natural_fibers
WHERE gots_compliant = true
ORDER BY name;

-- Insert initial model metadata
INSERT INTO models (name, version, architecture, training_dataset, is_active, trained_at) VALUES
('baseline_gnn', 'v1.0.0', 'SchNet', 'synthetic_dataset_v1', true, CURRENT_TIMESTAMP),
('quantum_enhanced', 'v1.1.0', 'SchNet+QuantumDescriptors', 'combined_dataset_v2', false, CURRENT_TIMESTAMP);

COMMIT; 