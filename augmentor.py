import Augmentor
from Augmentor.Operations import Operation
import PIL
import numpy as np
import random
np.set_printoptions(threshold=np.nan)

class SpeckleImage(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, images):
        arr = []
        for item in images:
            im = item.convert('RGBA')
            data = np.array(im)
            for row_idx, row in enumerate(data):
                for cell_idx, cell in enumerate(row):
                    if cell[0] == 0 and cell[1] == 0 and cell[2] == 0:
                        rnd_r = random.randint(1,255)
                        rnd_g = random.randint(1,255)
                        rnd_b = random.randint(1,255)
                        data[row_idx, cell_idx] = (rnd_r, rnd_g, rnd_b, 255)
            i = PIL.Image.fromarray(data)
            rgb_im = i.convert('RGB')
            arr.append(rgb_im)
        return arr

class TouchGrey(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, images):
        arr = []
        for item in images:
            im = item.convert('RGBA')
            data = np.array(im)
            for row_idx, row in enumerate(data):
                for cell_idx, cell in enumerate(row):
                    red, green, blue, a = cell
                    if (int(red) + int(green) + int(blue)) < 3:
                        data[row_idx, cell_idx] = (1, 1, 1, 255)
            i = PIL.Image.fromarray(data)
            rgb_im = i.convert('RGB')
            arr.append(rgb_im)
        return arr

speckle_image = SpeckleImage(probability = 1)
touch_grey = TouchGrey(probability = 1)

# train
p = Augmentor.Pipeline(source_directory="../medium_cards/3ed", output_directory="../../3ed_output")
p.add_operation(touch_grey)
p.random_brightness(probability=0.9, min_factor=0.65, max_factor=1.4)
p.resize(probability=1, width=610, height=800, resample_filter=u'BICUBIC')
p.zoom(probability=1, min_factor=0.55, max_factor=0.55)
p.rotate_without_crop(probability=1, max_left_rotation=90, max_right_rotation=90)
p.skew(probability=0.8, magnitude=0.15)
p.zoom(probability=1, min_factor=0.5, max_factor=1)
p.crop_by_size(probability=1, width=610, height=610, centre=True)
p.resize(probability=0.5, width=300, height=300, resample_filter=u'BILINEAR')
p.resize(probability=1, width=400, height=400, resample_filter=u'BICUBIC')
p.add_operation(speckle_image)
# p.greyscale(probability=1)
p.sample(10000)


# g = p.keras_generator(batch_size=1)
# images, labels = next(g)

# print('images')
# print(images)
# print('labels')
# print(labels)
