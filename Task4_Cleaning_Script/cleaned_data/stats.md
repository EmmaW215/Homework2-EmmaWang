# Data Cleaning Statistics

**Generated**: 2025-11-03 18:52:07

## Input Statistics

- **Total Documents Loaded**: 200
  - Task #1 (ArXiv): 0
  - Task #2 (OCR): 199
  - Task #3 (Transcripts): 1

- **Original Characters**: 15,550,035
- **Original Words**: 2,209,351
- **Original Tokens**: 2,209,351

## Cleaning Pipeline Results

1. **After Language Filter**: 198 documents
2. **After HTML Cleaning**: 198 documents
3. **After Deduplication**: 198 documents
4. **After PII Removal**: 198 documents
5. **After N-gram Filter**: 198 documents

## Output Statistics

- **Final Documents**: 198
- **Final Characters**: 14,334,465
- **Final Words**: 2,049,725
- **Final Tokens**: 2,049,725
- **Data Removed**: 7.23%

## Language Detection

| Language | Count |
|----------|-------|
| en | 198 |
| id | 1 |
| unknown | 1 |

## PII Patterns Removed

| Type | Count |
|------|-------|
| credit_card | 127 |
| email | 238 |
| phone | 58 |
| url | 1523 |

