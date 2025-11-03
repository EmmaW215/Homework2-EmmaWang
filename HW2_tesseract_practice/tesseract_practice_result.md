(venv) emmawang@mac tesseract_practice % python tesseract_practice.py

================================================================================
                    TESSERACT OCR PRACTICE EXERCISES
================================================================================

Available exercises:
  1. Exercise 1: Basic OCR
  2. Exercise 2: Preprocessing
  3. Exercise 3: PSM Modes
  4. Exercise 4: Confidence Scores
  5. Exercise 5: Invoice Extraction
  6. Exercise 6: Multilingual
  7. Bonus: Performance

Running all exercises...
(Update image paths in each function before running)


================================================================================
EXERCISE 1: BASIC OCR
============================================================
Extracted text:
Machine Learning &

Thisisasample text for OOR testing

Itcontains multiple lineswith differentcontent

Numbers 1234667800,

Specialcharacters @#9%%6«()

Invoice #12845

Date: 1102/2025

Total $1,23458,


Total words: 22

================================================================================

EXERCISE 2: PREPROCESSING
============================================================
Original:    203 chars
Grayscale:   203 chars
Threshold:   197 chars

================================================================================

EXERCISE 3: PSM MODES
============================================================

Invoice/Receipt (PSM 6):
  Characters: 196
  Preview: Machine Learning &
Thisisasample text for OOR test...

Single line (PSM 7):
  Characters: 2
  Preview: =
...

Paragraph (PSM 3):
  Characters: 203
  Preview: Machine Learning &

Thisisasample text for OOR tes...

Scattered text (PSM 11):
  Characters: 203
  Preview: Machine Learning &

Thisisasample text for OOR tes...

================================================================================

EXERCISE 4: CONFIDENCE SCORES
============================================================
Total detections: 21
Average confidence: 67.4%
Min confidence: 22%
Max confidence: 95%

⚠️  Low confidence detections (< 70%):
  'Thisisasample' - 22%
  'text' - 47%
  'for' - 47%
  'Itcontains' - 56%
  'multiple' - 46%
  'lineswith' - 38%
  'differentcontent' - 54%
  'Specialcharacters' - 65%
  '1102/2025' - 51%
  '$1,23458,' - 55%

================================================================================

EXERCISE 5: INVOICE DATA EXTRACTION
============================================================
Full extracted text:
Machine Learning &.Al
‘Trisisa sample text for OCR testing
Iteontains muttipis ineswith differenteontent
Numbers 1284667800
Specialcharactors @#S%ABe()
Invoios #12845
Date: 11/02/2025
Total $1.23458


📊 Extracted structured data:
  Invoice Number: Not found
  Date: 11/02/2025
  Total: 1.23458
  Tax: Not found

================================================================================

EXERCISE 6: MULTILINGUAL OCR
============================================================
Installed languages: afr, amh, ara, asm, aze, aze_cyrl, bel, ben, bod, bos, bre, bul, cat, ceb, ces, chi_sim, chi_sim_vert, chi_tra, chi_tra_vert, chr, cos, cym, dan, deu, div, dzo, ell, eng, enm, epo, equ, est, eus, fao, fas, fil, fin, fra, frk, frm, fry, gla, gle, glg, grc, guj, hat, heb, hin, hrv, hun, hye, iku, ind, isl, ita, ita_old, jav, jpn, jpn_vert, kan, kat, kat_old, kaz, khm, kir, kmr, kor, kor_vert, lao, lat, lav, lit, ltz, mal, mar, mkd, mlt, mon, mri, msa, mya, nep, nld, nor, oci, ori, osd, pan, pol, por, pus, que, ron, rus, san, sin, slk, slv, snd, snum, spa, spa_old, sqi, srp, srp_latn, sun, swa, swe, syr, tam, tat, tel, tgk, tha, tir, ton, tur, uig, ukr, urd, uzb, uzb_cyrl, vie, yid, yor

English result: 203 chars

================================================================================

BONUS: PERFORMANCE OPTIMIZATION
============================================================

Default:
  Time: 0.118s
  Output: 203 chars

Fast (PSM 7):
  Time: 0.056s
  Output: 2 chars

Accurate (PSM 6 + OEM 1):
  Time: 0.082s
  Output: 196 chars

⚡ Fastest: Fast (PSM 7) (0.056s)

================================================================================
✅ ALL EXERCISES COMPLETE!
================================================================================

📚 Next Steps:
  1. Download sample images from Google (invoices, receipts, documents)
  2. Run each exercise with different images
  3. Experiment with preprocessing parameters
  4. Compare PSM modes for your specific use case
  5. Build a mini-project: Receipt scanner or Document digitizer

💡 Tips:
  - Higher contrast = better OCR
  - Remove noise and blur for accuracy
  - Choose PSM based on document layout
  - Test multiple preprocessing combinations
  - Always check confidence scores