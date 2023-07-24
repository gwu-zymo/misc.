# install PIL 
# pip install pillow

from PIL import Image
import os

folder_path = './images/figures_for_report'  # Replace with the path to your folder

output_folder = 'images/figures_for_report'  # Replace with the path to the output folder
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        
        # Check if the image is in vertical orientation
        if image.height > image.width:
            # Rotate the image counter-clockwise by 90 degrees
            rotated_image = image.transpose(Image.ROTATE_270)
        else:
            rotated_image = image
        
        output_path = os.path.join(output_folder, filename)
        rotated_image.save(output_path)
        
