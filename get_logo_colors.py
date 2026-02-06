from PIL import Image
from collections import Counter
import os

def get_dominant_colors(image_path, num_colors=10):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        # Resize to speed up processing
        img = img.resize((100, 100))
        pixels = list(img.getdata())
        
        # Filter out whites/near-whites and blacks/near-blacks if needed, 
        # but let's see raw data first.
        
        counts = Counter(pixels)
        common = counts.most_common(num_colors)
        
        print(f"Dominant colors in {os.path.basename(image_path)}:")
        for color, count in common:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            print(f"- {hex_color} (RGB: {color})")
            
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    path = r"c:\Users\Nithi\.gemini\antigravity\NewNrconsultancybulid\assets\img\logo\logo-main.png"
    get_dominant_colors(path)
