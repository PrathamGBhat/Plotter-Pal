# Graph Plotter - User Guide

## What This Does
Takes your graph and data images, extracts the data, and prints it as a professional A4 graph sheet.

## Setup (One Time)

1. **Install Python packages:**
   ```
   pip install -r requirements.txt
   ```

## How to Use

### Option 1: Automatic (Uses AI to extract data)

1. Put expected graph image in `references/graph/` folder
2. Put value images in `references/values/` folder (max 5 images)
3. Run parser:
   ```
   python references/agent/gemini-parser.py
   ```
4. Run plotter:
   ```
   python plotter.py
   ```
5. Open `output.pdf`

### Option 2: Manual (Edit config.json)

1. Edit `config.json`:
   - Set `graphs` = number of curves
   - Set `limits` = axis ranges (xlim_start, xlim_end, ylim_start, ylim_end)
   - Set `scale` = units per cm (for grid squares)
   - Add your data points in `x-val-1`, `y-val-1`, `x-val-2`, `y-val-2`, etc.

2. Run plotter:
   ```
   python plotter.py
   ```
3. Open `output.pdf`

## File Structure

```
workspace/
├── config.json              (Data and settings)
├── plotter.py               (Makes the graph)
├── requirements.txt         (Python packages)
├── output.png               (Your printed graph as png)
├── output.pdf               (Your printed graph as pdf)
└── references/
    ├── graph/               (Put expected graph image here)
    └── values/              (Put data images here)
```

## Config.json Example

```json
{
    "orientation": "horizontal",
    "graphs": 2,
    "scale": {
        "x-axis-1-cm": 0.2,
        "y-axis-1-cm": 2
    },
    "limits": {
        "xlim_start": -0.8,
        "xlim_end": 3.6,
        "ylim_start": -20,
        "ylim_end": 14
    },
    "values": {
        "x-val-1": [0.0, 0.5, 1.0],
        "y-val-1": [1.0, 2.0, 3.0],
        "x-val-2": [0.1, 0.6, 1.1],
        "y-val-2": [1.5, 2.5, 3.5]
    }
}
```

## Settings Explained

- **orientation**: `"horizontal"` or `"vertical"` (A4 paper direction)
- **graphs**: Number of curves to plot
- **scale**: How many data units = 1 cm on printed page
- **limits**: Min/max values for each axis
- **values**: Your data points (x-val-N and y-val-N pairs)

## Output

`output.pdf` - Ready to print on A4 paper with:
- Green grid background
- Your data points as black dots
- Professional margins
- Square grid cells (1cm × 1cm)

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Wrong data extracted | Manually edit `config.json` |
| Graph looks wrong | Adjust `scale` and `limits` in config.json |
| No grid squares | Check `scale` values aren't zero |

## Tips

- **Scale**: Higher number = smaller grid squares
- **Limits**: Add 5-10% padding around your data
- **Multiple graphs**: Use indexed fields: x-val-1/2/3, y-val-1/2/3
