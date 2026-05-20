# Virtual Mouse

A Python-based virtual mouse that uses your computer's webcam to track hand gestures and control your mouse cursor. Built with OpenCV, MediaPipe, and PyAutoGUI.

## Features

- **Smooth Mouse Movement**: Maps the position of your index finger to the screen with built-in stabilization and dead-zones to reduce jitter.
- **Click Gesture**: Perform a "pinch" gesture (bringing your index finger and thumb together) to simulate a mouse click.
- **Adjustable Settings**: Easily tweak smoothing, dead-zones, and click thresholds at the top of the `main.py` script.

## Requirements

- Python 3.7 or higher
- A working webcam

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saireddy-shyamakura/virtual_mouse
   cd virtual_input
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. A window will open showing your webcam feed. 
3. Hold up your hand. The script will track your index finger to move the mouse cursor.
4. Pinch your index finger and thumb close together to perform a click.
5. Press the `ESC` key while the webcam window is in focus to stop the program.

## Configuration

You can customize the following variables in `main.py` to tune the virtual mouse to your preference:

- `smooth_x` & `smooth_y`: Controls the smoothness of the cursor movement (higher = smoother but slower).
- `frame_reduction`: Defines the boundary box within the webcam frame to improve reachability across the screen.
- `dead_zone`: The minimum distance the finger must move vertically to update the cursor (helps remove idle jitter).
- `click_threshold`: The maximum distance between the thumb and index finger to trigger a click.
- `click_delay`: The cooldown time (in seconds) between consecutive clicks.
