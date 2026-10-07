# YOLO Camera Guidance

A small Python application that uses Ultralytics YOLOv8 to detect people from a webcam and print basic position-based guidance in the terminal. Annotated predictions are displayed and saved for later review.

## Features

- Real-time person detection from the default webcam.
- Terminal guidance based on a person's horizontal position and bounding-box height: `TURN LEFT`, `TURN RIGHT`, `FORWARD`, or `BACKWARD`.
- Annotated prediction output saved by Ultralytics under `runs/detect/`.
- YOLOv8 nano model (`yolov8n.pt`) for lightweight inference.

These hints are experimental and use bounding-box geometry only. They are not a substitute for a navigation or safety system.

## Requirements

- Python 3.10 or later.
- A webcam for the default camera mode.
- A working camera backend and permission for the Python process to access the camera.

## Setup

Create and activate a virtual environment, then install the dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ultralytics
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

If you use Conda instead, create and activate a local environment with:

```bash
conda create --prefix .venv python=3.13 pip
conda activate ./.venv
python -m pip install ultralytics
```

The model file is expected at `yolov8n.pt` in the project directory. Ultralytics can download the model automatically on first use if it is not present.

## Run

With the environment activated:

```bash
python main.py
```

The application opens the camera, displays an annotated preview, and prints guidance for detected people. Press `q` in the preview window to stop. If the camera does not open, check that it is connected, available to other applications, and permitted by your operating system.

## Saved Results

Predictions are saved under `runs/detect/`. Ultralytics creates a new `predict` directory for each run when a previous one already exists. These generated outputs are excluded from Git by `.gitignore`.

## Troubleshooting

### `No module named 'ultralytics'`

Activate the project's environment, then install through that environment's Python:

```bash
source .venv/bin/activate
python -m pip install ultralytics
python -m pip show ultralytics
```

On Conda, activate the prefix with `conda activate ./.venv` first. Using `python -m pip` helps ensure the package is installed into the same environment that runs `main.py`.

### The camera does not open

Close other applications using the camera and check operating-system camera permissions. The script uses camera index `0` by default; if your camera has a different index, update the camera source in `main.py`. Camera access may also fail in remote, containerized, or headless sessions.

### The image path cannot be found

Use a path relative to the project directory or an absolute path, and check the spelling and file extension. For example, `Images/superman.png` refers to a file inside the project's `Images/` folder.

### The model cannot be loaded

Confirm that `yolov8n.pt` is in the project directory. If it is missing, Ultralytics may download it on first run; that requires an internet connection. Alternatively, set the model path to a weights file you already have.

### The preview window does not appear

The prediction call uses `show=True`, which requires a graphical desktop session. In a headless environment, disable preview display in `main.py` and use the saved output under `runs/detect/` instead.

### No people are detected

Try a well-lit image or scene with the person clearly visible and not too far from the camera. The project uses the lightweight `yolov8n.pt` model, so detection quality can vary with image conditions.

## Image Input

To run detection on an image instead of the webcam, set `relpath` near the top of `main.py` to an image path, for example:

```python
relpath = "Images/superman.png"
```

The image is displayed with detections and the annotated result is saved under `runs/detect/`. The terminal guidance loop currently runs only in webcam mode.

## Project Files

- `main.py` - Loads the model, runs inference, and prints person-position guidance.
- `Images/` - Example input images.
- `yolov8n.pt` - YOLOv8 nano model weights.
- `runs/` - Generated prediction output; ignored by Git.
