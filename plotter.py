import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# =====================================================
# Configuration Reader
# =====================================================

def load_config(config_file='config.json'):
    """Load configuration from config.json"""
    default_config = {
        'values': {
            'x-val': [],
            'y-val': []
        },
        'scale': {
            'x-axis-1-cm': 0.02,
            'y-axis-1-cm': 0.5
        },
        'limits': {
            'xlim_start': 0.1,
            'xlim_end': 0.606,
            'ylim_start': -0.5,
            'ylim_end': 8.3
        }
    }
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Merge with defaults for missing keys
        if 'values' not in config:
            config['values'] = default_config['values']
        if 'scale' not in config:
            config['scale'] = default_config['scale']
        if 'limits' not in config:
            config['limits'] = default_config['limits']
        
        return config
    except Exception as e:
        print(f"Warning: Could not load config.json ({e}). Using defaults.")
        return default_config

# Load configuration
config = load_config()

# =====================================================
# Data Input (from config)
# =====================================================

# Extract all indexed graph data
all_x = []
all_y = []

values = config['values']
index = 1

# Iterate through indexed x-val and y-val pairs
while f'x-val-{index}' in values and f'y-val-{index}' in values:
    x_data = values.get(f'x-val-{index}', [])
    y_data = values.get(f'y-val-{index}', [])
    
    # Only add if both exist and are non-empty
    if x_data and y_data:
        all_x.extend(x_data)
        all_y.extend(y_data)
        print(f"Loaded graph {index}: {len(x_data)} data points")
    
    index += 1

if not all_x or not all_y:
    print("Warning: No data found in config values.")
else:
    print(f"Total data points loaded: {len(all_x)}")

# =====================================================
# Plotting Configuration for A4 (Orientation from config)
# =====================================================

# Determine page dimensions based on orientation
orientation = config.get('orientation', 'horizontal').lower()

if orientation == 'vertical':
    # Portrait A4: 21.0 cm x 29.7 cm
    A4_WIDTH_CM = 21.0
    A4_HEIGHT_CM = 29.7
    print("Using Portrait (Vertical) A4 orientation")
else:
    # Landscape A4: 29.7 cm x 21.0 cm (default)
    A4_WIDTH_CM = 29.7
    A4_HEIGHT_CM = 21.0
    print("Using Landscape (Horizontal) A4 orientation")

# User specifications:
# Border on sides: 2.2 cm (left margin = 2.2 cm, right margin = 2.2 cm)
# Border top/bottom: 1.7 cm
#
# Axes box width = A4_WIDTH_CM - 2.2 - 2.2 cm
# Axes box height = A4_HEIGHT_CM - 1.7 - 1.7 cm

box_width_cm = A4_WIDTH_CM - 2.2 - 2.2
box_height_cm = A4_HEIGHT_CM - 1.7 - 1.7

left_cm = 2.2
bottom_cm = 1.7

# Convert to fractions of page dimensions
left_frac = left_cm / A4_WIDTH_CM
bottom_frac = bottom_cm / A4_HEIGHT_CM
width_frac = box_width_cm / A4_WIDTH_CM
height_frac = box_height_cm / A4_HEIGHT_CM

# Create the figure
paper_width_in = A4_WIDTH_CM / 2.54
paper_height_in = A4_HEIGHT_CM / 2.54

fig = plt.figure(figsize=(paper_width_in, paper_height_in), dpi=300)
ax = fig.add_axes([left_frac, bottom_frac, width_frac, height_frac])

# Load limits and scales from config
xlim_start = config['limits']['xlim_start']
xlim_end = config['limits']['xlim_end']
ylim_start = config['limits']['ylim_start']
ylim_end = config['limits']['ylim_end']

ax.set_xlim(xlim_start, xlim_end)
ax.set_ylim(ylim_start, ylim_end)

# Ticks configuration (1 cm major lines, 1 mm minor lines)
# x-axis: major tick from config, minor 1/10 of major
# y-axis: major tick from config, minor 1/10 of major

x_major_tick = config['scale']['x-axis-1-cm']
y_major_tick = config['scale']['y-axis-1-cm']

# Validate and fix zero/invalid scales
if x_major_tick <= 0:
    x_range = xlim_end - xlim_start
    x_major_tick = max(0.01, x_range / 12) if x_range > 0 else 0.1
    print(f"⚠ Warning: Invalid x-scale (0), using calculated value: {x_major_tick}")

if y_major_tick <= 0:
    y_range = ylim_end - ylim_start
    y_major_tick = max(0.01, y_range / 12) if y_range > 0 else 0.1
    print(f"⚠ Warning: Invalid y-scale (0), using calculated value: {y_major_tick}")

x_minor_tick = x_major_tick / 10
y_minor_tick = y_major_tick / 10

ax.set_xticks(np.arange(xlim_start, xlim_end + 1e-9, x_major_tick))
ax.set_xticks(np.arange(xlim_start, xlim_end + 1e-9, x_minor_tick), minor=True)

ax.set_yticks(np.arange(ylim_start, ylim_end + 1e-9, y_major_tick))
ax.set_yticks(np.arange(ylim_start, ylim_end + 1e-9, y_minor_tick), minor=True)

# Grid styling (standard green graph paper theme)
ax.grid(which='major', color='#2eb82e', linestyle='-', linewidth=0.5, alpha=0.8)
ax.grid(which='minor', color='#adebad', linestyle='-', linewidth=0.2, alpha=0.6)
ax.set_axisbelow(True)

# Remove all labels, titles, and numeric ticks/formatting
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_title("")
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.xaxis.set_minor_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_minor_formatter(plt.NullFormatter())

# Plot points as small filled black circles (size s=5), no connecting lines
ax.scatter(all_x, all_y, color='black', s=5, zorder=5)

# =====================================================
# Save Output
# =====================================================

# Save to output.pdf in the current workspace directory
output_path = os.path.join(os.path.dirname(__file__), 'output.pdf')
fig.savefig(output_path, format='pdf', dpi=300)
print(f"Output saved to: {output_path}")

# Also save PNG for preview
output_png = output_path.replace('.pdf', '.png')
fig.savefig(output_png, format='png', dpi=300)
print(f"Preview saved to: {output_png}")

plt.close(fig)
print("Done! Generated A4-formatted data points plot.")
