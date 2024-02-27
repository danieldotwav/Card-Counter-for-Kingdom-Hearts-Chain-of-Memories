import pygetwindow as gw
import pyautogui
from PIL import Image
import mss
import time
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

# Global Variables #

# Define RGB ranges for each color within +/- 10 of actual rgb values
color_ranges = {
    'red': ((200, 0, 0), (255, 50, 50)),       # RGB: rgb(214, 16, 0)
    'green': ((10, 175, 5), (30, 185, 15)),    # RGB: rgb(16, 181, 8)
    'blue': ((10, 50, 150), (40, 100, 200))    # RGB: rgb(24, 82, 181)
}

# Initialize counters for each color
color_counters = {'red': 0, 'green': 0, 'blue': 0}

application_title = "mGBA - Kingdom Hearts - Chain of Memories (USA)"
battle_started_reference_image_path = "C:/Users/daniel/Documents/Visual Studio Code/COM Card Counter/Resources/battle_indicator.png"
win = gw.getWindowsWithTitle(application_title)[0]

offsetX, offsetY = win.width // 2 - 100, win.height // 2 - 150
regionWidth, regionHeight = 200, 200
region = {"top": win.top + offsetY, "left": win.left + offsetX, "width": regionWidth, "height": regionHeight}


# Main Workflow #
def main() :
    center_window(application_title)  # Ensure the application window is centered
    capture_and_analyze_region()  # Capture and analyze the region of interest
    monitor_for_battle_start(application_title, battle_started_reference_image_path, region, similarity_threshold=0.8)

    # Display color counter for testing purposes
    print(color_counters)


# Methods #

# Logic for determining the beginning of a battle sequence
def compare_images(img1, img2):
    """Compute the similarity index between two images."""
    # Convert images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM between two images
    score, _ = ssim(img1_gray, img2_gray, full=True)
    return score

def capture_screenshot(region):
    """Capture a screenshot of the specified region."""
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX"))
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def is_color_within_range(color, color_range):
    return all(low <= color_component <= high for color_component, (low, high) in zip(color, zip(*color_range)))

def update_color_counters(color):
    """Increment the counter for the detected color."""
    for color_name, color_range in color_ranges.items():
        if is_color_within_range(color, color_range):
            color_counters[color_name] += 1
            print(f"\nIncremented {color_name} counter to {color_counters[color_name]}\n")
            break

def monitor_for_battle_start(application_title, reference_image_path, monitor_region, similarity_threshold=0.8):
    """Monitor for the battle start by comparing live screenshots to a reference image."""
    reference_image = cv2.imread(reference_image_path, cv2.IMREAD_COLOR)
    
    while True:
        current_screenshot = capture_screenshot(monitor_region)
        similarity_score = compare_images(current_screenshot, reference_image)
        
        if similarity_score >= similarity_threshold:
            # Similarity threshold met or exceeded, indicating battle start
            print("Battle start detected. Similarity score:", similarity_score)
            capture_and_analyze_region(application_title)
            break  # Or continue, depending on whether you want to keep monitoring
        
        time.sleep(0.1)  # Adjust based on how fast the animation occurs and system performance

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
    
def capture_and_analyze_region():
    try:
        if win:
            with mss.mss() as sct:
                save_path="cardcolor.png"
                sct_img = sct.grab(region)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img.save(save_path)
                center_pixel_color = img.getpixel((region['width'] // 2, region['height'] // 2))
                update_color_counters(center_pixel_color)
                print(f"Saved capture to {save_path}. Center Pixel Color: {center_pixel_color}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# Script Entry Point #
if __name__ == "__main__":
    main()