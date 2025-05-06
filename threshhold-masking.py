import os
import json
import numpy as np
import matplotlib.pyplot as plt
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# --- Step 1: File selection ---
Tk().withdraw()  # Hide the root Tk window
json_path = askopenfilename(title="Select the .json metadata file", filetypes=[("JSON files", "*.json")])


base_prefix = os.path.splitext(json_path)[0]
peak_path = f"{base_prefix}.peak"

if not os.path.isfile(peak_path):
    raise FileNotFoundError(f"Could not find corresponding .peak file at: {peak_path}")

print(f"Selected JSON: {json_path}")
print(f"Corresponding PEAK: {peak_path}")

# --- Step 2: Load metadata and data ---
with open(json_path, "r") as f:
    meta = json.load(f)

shape = tuple(meta["peakDimensions"]["Shape"])
y_coords = meta["peakDimensions"]["AxesCoords"][0]
polarizations = meta["peakDimensions"]["AxesCoords"][1]
x_coords = meta["peakDimensions"]["AxesCoords"][2]
channels = meta["peakDimensions"]["AxesCoords"][3]

data = np.fromfile(peak_path, dtype=np.float32).reshape(shape)

# --- Step 3: Visualization function ---
def plot_all_maps(data_array, title_suffix=""):
    n_pol = len(polarizations)
    n_ch = len(channels)

    fig, axes = plt.subplots(n_pol, n_ch, figsize=(3 * n_ch, 3 * n_pol), squeeze=False)

    for pol_idx in range(n_pol):
        for ch_idx in range(n_ch):
            ax = axes[pol_idx][ch_idx]
            intensity = data_array[:, pol_idx, :, ch_idx, 0]
            im = ax.imshow(intensity, extent=[min(x_coords), max(x_coords), min(y_coords), max(y_coords)],
                           origin="lower", aspect="auto", cmap="viridis", vmin=0, vmax=np.max(data))
            ax.set_title(f"Pol {polarizations[pol_idx]}°, Ch {channels[ch_idx]}")
            ax.set_xlabel("X [mm]")
            ax.set_ylabel("Y [mm]")

    fig.suptitle(f"Intensity Maps {title_suffix}", fontsize=16)
    fig.colorbar(im, ax=axes, orientation="vertical", shrink=0.6)
    plt.tight_layout()
    plt.show()

# --- Step 4: Plot original data ---
plot_all_maps(data, title_suffix="(Original)")

# --- Step 5: Apply threshold ---
threshold = 25
data_thresh = data.copy()
data_thresh[data_thresh < threshold] = 0

# --- Step 6: Plot thresholded data ---
plot_all_maps(data_thresh, title_suffix=f"(Thresholded @ {threshold})")

# --- Step 7: Save thresholded data ---
new_prefix = base_prefix + f"_THRESHOLD{threshold}"
new_peak_path = new_prefix + ".peak"
new_json_path = new_prefix + ".json"

data_thresh.astype(np.float32).tofile(new_peak_path)
shutil.copyfile(json_path, new_json_path)

print(f"\n✅ Saved thresholded .peak to: {new_peak_path}")
print(f"✅ Copied metadata .json to: {new_json_path}")
