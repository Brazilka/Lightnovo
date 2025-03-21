# Lightnovo
Scripts that I use in Lightnovo internship

1) size-analysis.py
For each `.png` image in the folder:
- 📊 Histogram with KDE overlay
- 📸 Preview of the binary processed image
- 📄 CSV file: `{sample_name}_particle_areas.csv`

1. **Reads the image** and converts it to grayscale.
2. **Applies Gaussian blur** to reduce noise.
3. **Performs automatic thresholding** (Otsu's method) to create a binary mask.
4. **Finds contours** (particles) and filters out tiny noise.
5. **Calculates particle area** in microns² based on real image scale.
6. **Displays results**:
   - Binary mask image
   - Histogram + KDE plot of particle areas
7. **Exports** area data to a CSV file per sample.

<!-- Image 1 -->
<img src="https://github.com/user-attachments/assets/177cad95-c65a-434f-9485-f969540ae2dd" alt="S1_200x200um" width="200" />

<!-- Image 2 -->
<img src="https://github.com/user-attachments/assets/aeb5a32c-d963-4539-b612-5ce62855d83f" alt="Figure 2025-03-21" width="200" />

<img src="https://github.com/user-attachments/assets/d68a3664-7778-4bbd-81f8-4c237897bea2" alt="Figure 2025-03-21" width="300" />


2) 
