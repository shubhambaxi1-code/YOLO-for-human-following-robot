# YOLO Camera Guidance

A Python application built with Ultralytics YOLOv8. It detects objects from a webcam or image. In camera mode, it also prints basic position-based guidance for detected people.

> **Safety note:** The guidance is experimental and based only on bounding-box size and position. Do not use it as a navigation, accessibility, or safety system.

## Features

- Detect objects using the YOLOv8 nano model (`yolov8n.pt`).
- Display annotated camera or image predictions.
- Save prediction output under `runs/detect/`.
- Print basic guidance for people detected by the camera: `FORWARD`, `BACKWARD`, `TURN LEFT`, `TURN RIGHT`, or `Idle`.

## Requirements

- Python 3.10 or later.
- A webcam for camera mode.
- A graphical desktop session to display prediction windows.
- Internet access on first run if Ultralytics needs to download `yolov8n.pt`.

## Setup

Create and activate a virtual environment, then install Ultralytics:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ultralytics
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run with a Camera

Run the application:

```bash
python main.py
```

The camera source is configured near the top of `main.py`:

```python
src = 0
```

Camera indexes start at `0`. For example, `0` selects the first camera and `1` selects a second camera if one is available. Use an integer for camera mode. The application currently does not enumerate or validate which camera indexes are available before starting YOLO; an invalid or inaccessible index may produce backend warnings instead of a clean `ConnectionError`.

The camera window is displayed and annotated predictions are saved under `runs/detect/`. Press `q` in the preview window to stop. Pressing Ctrl+C in the terminal is also handled as a stop request.

## Run with an Image

In `main.py`, set `src` to an image path string instead of an integer:

```python
src = "Images/superman.png"
```

Use a path relative to the project directory or an absolute path. Image predictions are displayed and saved under `runs/detect/`. The position-based guidance is only implemented in camera mode.

Example images are in the `Images/` directory.

## Results and Model

Ultralytics writes annotated predictions to `runs/detect/`, typically creating a new `predict` directory for each run. These generated results are ignored by Git.

The application loads `yolov8n.pt` from the project directory. If the weights are not present, Ultralytics may download them on first use. That requires an internet connection.

## Troubleshooting

### `No module named 'ultralytics'`

Activate the project environment, then install the package into that environment:

```bash
source .venv/bin/activate
python -m pip install ultralytics
```

### The camera preview does not open

Check that the camera is connected, not already in use by another application, and permitted by the operating system. Try camera index `0` first. Camera access may not work in remote, containerized, or headless sessions.

An invalid camera index can cause Ultralytics/OpenCV warnings such as `Waiting for stream`. Those warnings are not necessarily Python `ConnectionError` exceptions, so the current exception handler may not catch them.

### The image cannot be found

Check the spelling, file extension, and path. For example, `Images/superman.png` is relative to the project directory.

### No person is detected

Try a well-lit scene with the person clearly visible. Detection quality depends on distance, lighting, occlusion, and the model. Camera guidance is printed only for detections whose confidence is above the configured threshold in `classcamera.py`.

## Project Structure

| File or directory | Purpose |
| --- | --- |
| `main.py` | Loads the model and selects camera or image mode. |
| `classcamera.py` | Runs camera predictions and prints person-position guidance. |
| `classimage.py` | Runs image predictions. |
| `Images/` | Example image inputs. |
| `yolov8n.pt` | YOLOv8 nano model weights. |
| `runs/` | Generated prediction output; ignored by Git. |