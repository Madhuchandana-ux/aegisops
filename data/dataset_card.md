# AegisOps Dataset Card

## Project

AegisOps 2.0 - Production-Grade Agentic AI for Autonomous IT Incident Resolution

## Purpose

The datasets used by AegisOps support:

- IT incident classification
- Incident priority prediction
- Retrieval-augmented incident resolution
- Agent evaluation
- Resolution recommendation

## Dataset Sources

External datasets will be documented here before being used for
model training or evaluation.

## Data Provenance

For every external dataset, record:

- Dataset name
- Original source
- Original URL
- Publisher/organization
- License
- Date accessed
- Original filename
- Number of records
- Original fields
- AegisOps field mapping
- Known limitations

## Data Handling

Original external datasets are stored under:

data/raw/external/

The original files must not be modified.

Processed or transformed versions are stored under:

data/processed/external/

## Privacy

Potential personally identifiable information (PII) must not be exposed
through the application, logs, evaluation reports, or repository.

Any dataset containing sensitive or identifiable information must be
reviewed before use.

## Development Fixture

data/raw/incidents.csv is a small development fixture created for
testing the AegisOps pipeline.

It is NOT considered the final real-world training dataset.