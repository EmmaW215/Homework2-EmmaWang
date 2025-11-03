(venv) emmawang@mac tesseract_practice % python tesseract_tutorial.py
================================================================================
                    TESSERACT OCR TUTORIAL
               Best Practices & Practical Examples
================================================================================
✅ Tesseract is installed and working!

📝 Creating sample test image...
✅ Sample image created: /Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/sample_text.png

================================================================================
SECTION 1: IMAGE PREPROCESSING
================================================================================

============================================================
PREPROCESSING: GRAYSCALE
============================================================
Original image shape: (2955, 4470, 3)
✓ Converted to grayscale

============================================================
PREPROCESSING: THRESHOLD
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding

============================================================
PREPROCESSING: DENOISE
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied denoising

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

✅ Visualization saved to '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/preprocessing_comparison.png'

================================================================================
SECTION 2: PAGE SEGMENTATION MODES (PSM)
================================================================================

============================================================
PSM MODE COMPARISON
============================================================

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

PSM 3: Fully automatic (Default)
Text length: 966 characters
Preview: Original

Image Preprocessing Comparison

Grayscale

Adaptive Threshold

Original
nas Pence pn napst...

PSM 4: Single column
Text length: 956 characters
Preview: Original

Original

Image Preprocessing Comparison

Grayscale
nae epee

Adaptive Threshold

Denoised...

PSM 6: Single uniform block
Text length: 912 characters
Preview: | Preprocessing Comparison
Image Preprocessing Comparison Image Preprocessing Comparison Image Prepr...

PSM 7: Single text line
Text length: 10 characters
Text: i 7 : - =


PSM 11: Sparse text
Text length: 1679 characters
Preview: Image Preprocessing Comparison

Original

Grayscale

Adaptive Threshold

Image Preprocessing Compari...

PSM 13: Raw line
Text length: 2 characters
Text: a


============================================================
DETAILED OCR ANALYSIS (PSM=6)
============================================================

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

Total detections: 134
Valid detections (conf > 60%): 51

Top 10 detected words:
Text                 Confidence   Position (x,y)
------------------------------------------------------------
Preprocessing        96.0         (1914, 30)
Comparison           96.0         (2397, 30)
Image                75.0         (572, 390)
Preprocessing        96.0         (646, 389)
Comparison           96.0         (802, 389)
Image                75.0         (2057, 390)
Preprocessing        96.0         (2131, 389)
Comparison           96.0         (2287, 389)
Image                95.0         (3542, 390)
Preprocessing        96.0         (3616, 389)

============================================================
PREPROCESSING: GRAYSCALE
============================================================
Original image shape: (2955, 4470, 3)
✓ Converted to grayscale

✅ Bounding boxes saved to '/Users/emmawang/AI_Projects/VicEdu_ML/HW2_DataCollectionExtraction/tesseract_practice/bounding_boxes.png'

================================================================================
SECTION 3: LANGUAGE SUPPORT
================================================================================

============================================================
AVAILABLE LANGUAGES
============================================================

Total languages installed: 126

Language codes:
   1. afr
   2. amh
   3. ara
   4. asm
   5. aze
   6. aze_cyrl
   7. bel
   8. ben
   9. bod
  10. bos
  11. bre
  12. bul
  13. cat
  14. ceb
  15. ces
  16. chi_sim
  17. chi_sim_vert
  18. chi_tra
  19. chi_tra_vert
  20. chr
  21. cos
  22. cym
  23. dan
  24. deu
  25. div
  26. dzo
  27. ell
  28. eng
  29. enm
  30. epo
  31. equ
  32. est
  33. eus
  34. fao
  35. fas
  36. fil
  37. fin
  38. fra
  39. frk
  40. frm
  41. fry
  42. gla
  43. gle
  44. glg
  45. grc
  46. guj
  47. hat
  48. heb
  49. hin
  50. hrv
  51. hun
  52. hye
  53. iku
  54. ind
  55. isl
  56. ita
  57. ita_old
  58. jav
  59. jpn
  60. jpn_vert
  61. kan
  62. kat
  63. kat_old
  64. kaz
  65. khm
  66. kir
  67. kmr
  68. kor
  69. kor_vert
  70. lao
  71. lat
  72. lav
  73. lit
  74. ltz
  75. mal
  76. mar
  77. mkd
  78. mlt
  79. mon
  80. mri
  81. msa
  82. mya
  83. nep
  84. nld
  85. nor
  86. oci
  87. ori
  88. osd
  89. pan
  90. pol
  91. por
  92. pus
  93. que
  94. ron
  95. rus
  96. san
  97. sin
  98. slk
  99. slv
  100. snd
  101. snum
  102. spa
  103. spa_old
  104. sqi
  105. srp
  106. srp_latn
  107. sun
  108. swa
  109. swe
  110. syr
  111. tam
  112. tat
  113. tel
  114. tgk
  115. tha
  116. tir
  117. ton
  118. tur
  119. uig
  120. ukr
  121. urd
  122. uzb
  123. uzb_cyrl
  124. vie
  125. yid
  126. yor

============================================================
OCR WITH LANGUAGE: ENG
============================================================

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

✅ Successfully extracted text in 'eng'
Text length: 912 characters

Extracted text:
------------------------------------------------------------
| Preprocessing Comparison
Image Preprocessing Comparison Image Preprocessing Comparison Image Preprocessing Comparison
Original Grayscale Adaptive Threshold Original Grayscale Adaptive Threshold Original Grayscale Adaptive Threshold
sve ch Con Anup hepenin Coention nee eg pan sve ch Con Anup hepenin Coention nee eg pan snag ec Can Inosehepceing Conon nee eda gto
Denoised Full Preprocessing Denoised Full Preprocessing Denoised Full Preprocessing
snr rnc npn inspumnensinCoentinn sve racy Corin inspumnensinCoentinn son rca Contin ‘neve tprceing onrizn
Image Preprocessing Comparison Image Preprocessing Comparison
Original Grayscale Adaptive Threshold Original Grayscale Adaptive Threshold
see ca pron Anup hepenin Coention nee eg pan snag ec Can Inosehepceing Conon nee eda gto
Denoised Full Preprocessing Denoised Full Preprocessing
sro racy Corin inspumnensinCoentinn son rca Contin ‘neve tprceing onrizn

------------------------------------------------------------

================================================================================
SECTION 4: PERFORMANCE COMPARISON
================================================================================

============================================================
PERFORMANCE COMPARISON
============================================================

============================================================
PREPROCESSING: GRAYSCALE
============================================================
Original image shape: (2955, 4470, 3)
✓ Converted to grayscale

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

============================================================
PREPROCESSING: ALL
============================================================
Original image shape: (2955, 4470, 3)
✓ Applied adaptive thresholding
✓ Applied denoising

Method                    Time (s)     Chars      Preview
--------------------------------------------------------------------------------
No preprocessing          2.026        599        Original  Image Preprocessing Comparison  Original
Grayscale only            1.826        599        Original  Image Preprocessing Comparison  Original
Full preprocessing        8.420        966        Original  Image Preprocessing Comparison  Grayscal
Full + PSM 6              1.378        912        | Preprocessing Comparison Image Preprocessing Com
Full + PSM 11             1.706        1679       Image Preprocessing Comparison  Original  Grayscal

================================================================================
✅ TUTORIAL COMPLETE!
================================================================================

Generated files:
  - preprocessing_comparison.png
  - bounding_boxes.png
  - sample_text.png

Next steps:
  1. Try with your own images
  2. Experiment with different PSM modes
  3. Install additional language packs
  4. Fine-tune preprocessing parameters