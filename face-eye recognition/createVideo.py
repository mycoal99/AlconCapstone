import numpy as np
from PIL import Image
import cv2
import os
import imageio

if __name__ == "__main__":
    write_to = "C:\\Users\\Michael\\Desktop\\video\\demo2.mp4"
    image_folder = 'C:\\Users\\Michael\\Desktop\\video'
    writer = imageio.get_writer(write_to, format='mp4', mode='I', fps=2)
    images = [img for img in os.listdir(image_folder) if (img.endswith('.png') and img.startswith("EyeDectection"))]
    for i in range(len(images)):
        name = 'C:\\Users\\Michael\\Desktop\\video\\EyeDectection-' + str(i) + '.png'
        img = Image.open(name)
        writer.append_data(np.asarray(img))
    writer.close()    