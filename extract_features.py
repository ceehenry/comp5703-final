# This file is used to define a class that can extract the features from images
# There are 2 functions in class: 1. extract the normal features which uses the VGG16 pre-trained model form Keras
# frameworks, this is deep learning part 2. extract the color which gets the rgb data after converting to thumbnails

from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
from numpy import linalg as LA
import colorsys


class ExtractFeature:
    def __init__(self):
        model = VGG16(weights='imagenet')
        self.model = Model(inputs=model.input, outputs=model.get_layer('fc1').output)

    def extract(self, img):
        # initial the images
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert('RGB')  # Make sure img is color
        # processing the images
        x = image.img_to_array(img)  # To np.array. Height x Width x Channel. dtype=float32
        x = np.expand_dims(x, axis=0)  # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = preprocess_input(x)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )

        return feature / LA.norm(feature)

    def color(self, image):
        # convert images to RGBA
        image = image.convert('RGBA')
        # release the cpu
        image.thumbnail((200, 200))
        max_score = None
        dominant_color = None
        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # ignore the black
            if a == 0:
                continue
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)
            # ignore more than threshold
            if y > 0.9:
                continue
            # Calculate the score, preferring highly saturated colors.
            # Add 0.1 to the saturation so we don't completely ignore grayscale
            # colors by multiplying the count by zero, but still give them a low
            # weight.
            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)
        return dominant_color
