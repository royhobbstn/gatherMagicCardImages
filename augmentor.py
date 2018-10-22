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
                        rnd = random.randint(1,255) # b&w
                        data[row_idx, cell_idx] = (rnd, rnd, rnd, 255)
            i = PIL.Image.fromarray(data)
            rgb_im = i.convert('RGB')
            arr.append(rgb_im)
        return arr

class SharpCorners(Operation):
    def __init__(self, probability):
        Operation.__init__(self, probability)

    def perform_operation(self, images):
        arr = []
        for item in images:
            im = item.convert('RGBA')
            data = np.array(im)
            sample_cell = data[20, 20]
            sample_pixel = sample_cell[0]
            white_border = sample_pixel > 127
            for row_idx, row in enumerate(data):
                if row_idx < 20 or row_idx > 660:
                    for cell_idx, cell in enumerate(row):
                        red, green, blue, a = cell
                        if white_border:
                            if (int(red) + int(green) + int(blue)) < 383:
                                data[row_idx, cell_idx] = (0, 0, 0, 255)
                            else:
                                data[row_idx, cell_idx] = sample_cell
                        else:
                            if (int(red) + int(green) + int(blue)) < 383:
                                data[row_idx, cell_idx] = sample_cell
                            else:
                                data[row_idx, cell_idx] = (0, 0, 0, 255)
            i = PIL.Image.fromarray(data)
            rgb_im = i.convert('RGB')
            arr.append(rgb_im)
        return arr

speckle_image = SpeckleImage(probability = 1)
sharp_corners = SharpCorners(probability = 1)


p = Augmentor.Pipeline(source_directory="../aug_cards")
p.add_operation(sharp_corners)
p.random_brightness(probability=0.9, min_factor=0.65, max_factor=1.4)
p.resize(probability=1, width=610, height=800, resample_filter=u'BICUBIC')
p.zoom(probability=1, min_factor=0.55, max_factor=0.55)
p.rotate_without_crop(probability=1, max_left_rotation=90, max_right_rotation=90)
p.skew(probability=0.8, magnitude=0.15)
p.zoom(probability=1, min_factor=0.5, max_factor=1)
p.crop_by_size(probability=1, width=610, height=610, centre=True)
p.resize(probability=1, width=400, height=400, resample_filter=u'BICUBIC')
p.greyscale(probability=1)
p.add_operation(speckle_image)

p.sample(20)



# g = p.keras_generator(batch_size=1)
# images, labels = next(g)

# print('images')
# print(images)
# print('labels')
# print(labels)
