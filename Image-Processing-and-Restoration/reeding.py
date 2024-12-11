import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

def apply_reeded_piecewise_filter(image_path, strip_width=20, distortion_intensity=10):
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert to RGB (OpenCV uses BGR by default)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Get image dimensions
    _, width, _ = img_rgb.shape # height, width, channels, for now I am only utilizing the width to manipulate the vertical strips and apply the ripple/reed effect
    
    # Initialize a new empty image
    new_img = np.zeros_like(img_rgb)

    # Iterate over the image by column strips
    for i in range(0, width, strip_width):
        # Define the strip
        start_x = i
        end_x = min(i + strip_width, width)
        strip = img_rgb[:, start_x:end_x]

        # Apply a mirroring or distortion effect to the strip
        if (i // strip_width) % 2 == 0:
            # For every second strip, apply a mirroring effect
            strip = np.fliplr(strip)
        else:
            # Apply a slight vertical distortion to simulate the reed-like effect
            distortion = np.sin(np.linspace(0, np.pi, strip.shape[0])) * distortion_intensity
            distorted_strip = np.copy(strip)
            for row in range(strip.shape[0]):
                distorted_strip[row] = np.roll(strip[row], int(distortion[row]))
            strip = distorted_strip
        
        # Place the modified strip back into the new image
        new_img[:, start_x:end_x] = strip
    
    # Convert back to a PIL image for display
    pil_image = Image.fromarray(new_img)
    return pil_image

# Example usage
image_path = 'test-images/882367-winnie-the-pooh-blood-and-honey-0-1000-0-1500-crop.jpg'
reeded_image = apply_reeded_piecewise_filter(image_path)

# Display the result
plt.imshow(reeded_image)
plt.axis('off')
plt.show()
