import pygetwindow as gw
import pyautogui

from PIL import Image
import mss

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
    
def capture_application_region(title, save_path="capture.png"):
    try:
        win = gw.getWindowsWithTitle(title)[0]  # Assume gw is defined and imported correctly
        if win:
            # Adjust these values based on the offset and size of the target region within the app
            offsetX, offsetY = 100, 100  # Example offsets from the top-left corner of the window
            regionWidth, regionHeight = 200, 200  # Size of the region to capture
            
            with mss.mss() as sct:
                monitor = {
                    "top": win.top + offsetY,
                    "left": win.left + offsetX,
                    "width": regionWidth,
                    "height": regionHeight
                }
                sct_img = sct.grab(monitor)
                
                # Convert to PIL.Image for easier manipulation
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                
                # Save the image for visual inspection
                img.save(save_path)
                print(f"Saved capture to {save_path}")
    except Exception as e:
        print(f"Error: {e}")


# First, center the application screen
center_window("mGBA - Kingdom Hearts - Chain of Memories (USA)")

# We'll need more testing to get the exact location of the card colors
# These will be baseline values for our crude approximation of the card color location

left = 100  # Distance from the left edge of the screen
top = 100   # Distance from the top edge of the screen
width = 200 # Width of the capture region
height = 150 # Height of the capture region