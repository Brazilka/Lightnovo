# Lightnovo
Scripts that I use in Lightnovo internship

1) size-analysis.py
1. **Reads the image** and converts it to grayscale.
2. **Applies Gaussian blur** to reduce noise.
3. **Performs automatic thresholding** (Otsu's method) to create a binary mask.
4. **Finds contours** (particles) and filters out tiny noise.
5. **Calculates particle area** in microns² based on real image scale.
6. **Displays results**:
   - Binary mask image
   - Histogram + KDE plot of particle areas
7. **Exports** area data to a CSV file per sample.

2) threshhold-masking.py
1. **Interactively select** a `.json` metadata file describing spectroscopic peak data.
2. **Load and visualize** integrated intensity maps for all polarization states and spectral channels.
3. **Apply a threshold** to suppress noise or background (intensity values below 25 are set to zero).
4. **Re-visualize** the thresholded data.
5. **Exports** the thresholded dataset as a new `.peak` binary file and copy the corresponding `.json` file with a consistent name.
