import pygetwindow as gw
import pyautogui
from PIL import Image
import mss

# Initialize counters for each color
color_counters = {'red': 0, 'green': 0, 'blue': 0}

# Define RGB ranges for each color
color_ranges = {
    'red': ((200, 0, 0), (255, 50, 50)),
    'green': ((0, 200, 0), (50, 255, 50)),
    'blue': ((0, 0, 200), (50, 50, 255))
}

def is_color_within_range(color, color_range):
    return all(low <= color_component <= high for color_component, (low, high) in zip(color, zip(*color_range)))

def center_window(title):
    try:
        # Find the window by title
        win = gw.getWindowsWithTitle(title)[0]  # This gets the first window that matches the title.
        if win:
            # Get screen and window dimensions
            screenWidth, screenHeight = pyautogui.size()
            windowWidth, windowHeight = win.width, win.height
            
            # Calculate the center position
            centerX = (screenWidth - windowWidth) // 2
            centerY = (screenHeight - windowHeight) // 2
            
            # Move the window to the center
            win.moveTo(centerX, centerY)
    except Exception as e:
        print(f"Error: {e}")

def get_center_pixel_color(screen_width, screen_height):
    with mss.mss() as sct:
        # Create a dictionary to represent the portion of the screen to be captured
        monitor = {"top": screen_height // 2, "left": screen_width // 2, "width": 1, "height": 1}
        sct_img = sct.grab(monitor)

        # Convert to PIL.Image for easier manipulation
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # Get pixels
        return img.getpixel((0,0))
    
def capture_and_analyze_region(title, save_path="capture.png"):
    try:
        win = gw.getWindowsWithTitle(title)[0]
        if win:
            # Calculate the region to capture, e.g., center of the window
            region = calculate_capture_region(win)
            with mss.mss() as sct:
                sct_img = sct.grab(region)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img.save(save_path)
                center_pixel_color = img.getpixel((region['width'] // 2, region['height'] // 2))
                update_color_counters(center_pixel_color)
                print(f"Saved capture to {save_path}. Center Pixel Color: {center_pixel_color}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

def calculate_capture_region(win):
    """Calculate the region to capture based on the window position and size."""
    offsetX, offsetY = win.width // 2 - 100, win.height // 2 - 150
    regionWidth, regionHeight = 200, 200
    return {"top": win.top + offsetY, "left": win.left + offsetX, "width": regionWidth, "height": regionHeight}

def update_color_counters(color):
    """Increment the counter for the detected color."""
    for color_name, color_range in color_ranges.items():
        if is_color_within_range(color, color_range):
            color_counters[color_name] += 1
            print(f"\nIncremented {color_name} counter to {color_counters[color_name]}\n")
            break


# Main Workflow
application_title = "mGBA - Kingdom Hearts - Chain of Memories (USA)"
center_window(application_title)  # Ensure the application window is centered
capture_and_analyze_region(application_title, "cardcolor.png")  # Capture and analyze the region of interest

# Display color counter for testing purposes
print(color_counters)