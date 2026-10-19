# AegisOps Classifier Evaluation

## Objective

Evaluate the IT incident classifier using a grouped validation
split and a separate overlap-filtered test set.

## Model

- Word-level TF-IDF features
- Character-level TF-IDF features
- FeatureUnion to combine both feature sets
- Linear Support Vector Classifier (LinearSVC)
- Class-weight balancing for imbalanced categories

## Grouped validation results

The word-plus-character TF-IDF model achieved:

| Metric | Result |
|---|---:|
| Accuracy | 0.8379 |
| Macro F1 | 0.7762 |
| Weighted F1 | 0.8343 |

These are grouped validation results, not final test results.

## Final overlap-filtered test results

| Metric | Result |
|---|---:|
| Test records | 530 |
| Accuracy | 0.8113 |
| Macro F1 | 0.7681 |
| Weighted F1 | 0.8073 |

The test set was filtered to remove records whose normalized
descriptions also appeared in the training set.

## Evaluation limitations

- The original test split contained 657 records.
- Filtering exact normalized-description overlaps removed 127
  records, leaving 530 records.
- All 58 EOL test records overlapped with training descriptions.
- Therefore, the filtered test set contains no EOL examples.
- EOL performance cannot be measured from this filtered test set.
- The original test split contains repeated text templates and
  should not be presented as an unseen-description benchmark.
- Grouped validation and final test results are reported separately.

## Reproducibility

Use the repository's dataset preparation, grouped validation,
and final classifier training scripts to reproduce the evaluation.
Confirm the required input files and environment before running
the scripts.

## Interpretation

The results measure classification performance on the specified
splits. They do not establish production impact, calibrated
prediction probabilities, or performance on unseen EOL wording.
