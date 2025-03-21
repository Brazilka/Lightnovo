import sys
print(sys.executable)

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import gaussian_kde

def extract_metadata_from_filename(filename):
    """Extracts sample name and dimensions from the filename."""
    basename = os.path.basename(filename).replace(".png", "")
    parts = basename.split("_")
    sample_name = parts[0]  # e.g., 'S0', 'S1', 'S3'
    dimensions = parts[1].replace("um", "").split("x")
    width_um, height_um = int(dimensions[0]), int(dimensions[1])
    return sample_name, width_um, height_um

def process_image(image_path, width_um, height_um):
    """Processes an image to extract particle areas."""
    # Load image
    image = cv2.imread(image_path)
    
    # Convert to grayscale if not already
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Preprocessing (denoise & thresholding)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours (particles)
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Compute pixel-to-micron conversion
    image_height_px, image_width_px = image.shape
    pixel_to_micron_sq = (width_um / image_width_px) * (height_um / image_height_px)
    
    # Compute particle areas in µm²
    particle_areas = [cv2.contourArea(cnt) * pixel_to_micron_sq for cnt in contours if cv2.contourArea(cnt) > 5]
    
    return binary_mask, particle_areas

def analyze_folder(folder_path):
    """Processes all PNG images in a folder and performs particle analysis."""
    results = {}
    
    # Loop through all PNG files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            sample_name, width_um, height_um = extract_metadata_from_filename(filename)
            
            # Process image
            processed_image, particle_areas = process_image(file_path, width_um, height_um)
            results[sample_name] = results.get(sample_name, []) + particle_areas
            
            # Display processed image
            plt.figure(figsize=(6, 6))
            plt.imshow(processed_image, cmap='gray')
            plt.title(f"Processed Image: {sample_name} ({width_um}x{height_um} µm)")
            plt.axis("off")
            plt.axis("equal")
            plt.show()
    
    # Generate histograms for each sample group
    for sample, areas in results.items():
        plt.figure(figsize=(8, 5))
        plt.hist(areas, bins=20, edgecolor="black", alpha=0.7, density=True)

        # KDE for smooth visualization
        kde = gaussian_kde(areas)
        x_vals = np.linspace(min(areas), max(areas), 100)
        plt.plot(x_vals, kde(x_vals), color="red", lw=2, label="KDE")

        # Add total particle count
        total_particles = len(areas)
        plt.annotate(f"Total Particles: {total_particles}", xy=(0.7, 0.9), xycoords='axes fraction',
                     fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

        plt.xlabel("Particle Area (µm²)")
        plt.ylabel("Density")
        plt.title(f"Particle Area Distribution for {sample}")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    # Save particle area data
    for sample, areas in results.items():
        df = pd.DataFrame(areas, columns=["Area (µm²)"])
        df.to_csv(f"{folder_path}/{sample}_particle_areas.csv", index=False)
        print(f"Saved: {sample}_particle_areas.csv")

# Example usage
folder_path = r"C:\Users\LN\Desktop\experiments\distribution analysis"  
analyze_folder(folder_path)
