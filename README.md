# Card Counter for Kingdom Hearts - Chain of Memories

This Python project is designed to automate the process of counting specific color occurrences on the screen while playing "Kingdom Hearts - Chain of Memories" on the mGBA emulator. The script captures screenshots, analyzes specific regions for color patterns, and detects the start of battle sequences by comparing the current screen to a reference image.

## Features

- **Automatic Battle Detection**: Utilizes image comparison to detect the start of battles.
- **Color Counting**: Identifies and counts occurrences of predefined colors within a specified screen region.
- **Dynamic Window Handling**: Centers the emulator window and monitors specific regions for analysis.

## Requirements

To run this script, you will need Python installed on your system along with the following packages:
- pygetwindow
- pyautogui
- Pillow (PIL)
- mss
- scikit-image
- OpenCV-python (cv2)
- NumPy

You can install these packages using pip:

```sh
pip install pygetwindow pyautogui Pillow mss scikit-image opencv-python numpy
```

## Usage

1. **Set Up**: Ensure the mGBA emulator is running "Kingdom Hearts - Chain of Memories". Adjust the `application_title` variable if necessary to match your emulator's window title.
2. **Configure**: The script includes predefined RGB color ranges for red, green, and blue. You can modify these ranges in the `color_ranges` dictionary.
3. **Run**: Execute the script with Python. It will automatically center the emulator window, monitor for the start of battles, and count color occurrences.

## How It Works

1. **Center Window**: On startup, the script centers the emulator window on your screen, ensuring that the area of interest remains consistent for screenshot analysis.
2. **Monitor for Battle Start**: It continuously captures screenshots of a specified region, comparing them to a reference image to detect the beginning of a battle. This process relies on structural similarity indexing to determine when the game screen matches the pre-defined battle start indicator.
3. **Capture and Analyze Region**: Once a battle starts, the script captures and analyzes a predefined region of the screen for specified colors, updating counters for each identified color. This is crucial for tracking occurrences of certain colors during gameplay.
4. **Color Counting**: The script uses RGB color ranges defined in the `color_ranges` dictionary to identify specific colors on the screen. When a matching color is detected, its corresponding counter is incremented. This feature allows for the tracking of color-based events or items within the game.

## Configuration

- `color_ranges`: This dictionary defines the RGB ranges for red, green, and blue colors. Adjust these ranges as needed to match the specific colors you wish to track during gameplay.
- `application_title`: Specifies the title of the emulator window. It's crucial that this matches exactly with the window title of your running emulator to ensure the script functions correctly.
- `battle_started_reference_image_path`: Indicates the path to the reference image used by the script to detect the start of battles. This image should be a representative screenshot of what the game displays at the start of a battle.

## Note

This script is specifically tailored for "Kingdom Hearts - Chain of Memories" played on the mGBA emulator and might require adjustments for optimal performance, such as modifying the RGB color ranges or the region of the screen to be analyzed.

This program is nowhere near ready for deployment as an application, and would require extensive testing before being used in a speedrunning setting.

## Disclaimer

This project is intended for educational purposes and personal use. Please respect the copyright and usage rights of all software and games involved.