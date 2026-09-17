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
## External Dataset 1

### Name

Classification of IT Support Tickets

### Publisher

Zenodo

### Authors

Leonardo Santiago Benitez Pereira

### Source

https://zenodo.org/records/7648117

### DOI

10.5281/zenodo.7648117

### Dataset Size

2,229 IT support tickets.

### Origin

The tickets were obtained from an IT support company in the
Florianópolis region of Brazil.

### Classification

The tickets were manually classified into seven categories by
three IT support professionals.

### Privacy

The dataset documentation states that personally identifiable
information and sensitive information were removed and that the
result was manually verified.

### License

CC BY

### Intended Use in AegisOps

The dataset will be used for:

- Incident text classification
- Category prediction
- Classification benchmarking
- Agent routing experiments

### Important Limitation

The dataset is an IT support-ticket corpus rather than a complete
ServiceNow incident lifecycle dataset. It therefore does not
provide all fields required for priority prediction, incident
lifecycle analysis, ServiceNow action execution, or resolution
verification.

The dataset will therefore not be treated as a complete representation
of enterprise ServiceNow incidents.

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