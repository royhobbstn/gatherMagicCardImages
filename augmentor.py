import Augmentor
from Augmentor.Operations import Operation
import PIL
import numpy as np
import random
np.set_printoptions(threshold=np.nan)

class SpeckleImage(Operation):
    def __init__(self, probability, threshold, corners_only):
        Operation.__init__(self, probability)
        self.threshold = threshold
        self.corners_only = corners_only

    def perform_operation(self, images):
        arr = []
        for item in images:
            data = np.array(item).astype('uint8')
            data = PIL.Image.fromarray(data)
            im = data.convert('RGBA')
            data = np.array(im)
            red, green, blue, a = data.T
            black_areas = (red < 100) & (blue < 100) & (green < 100)
            data[..., :-1][black_areas.T] = (255, 0, 0)
#             for row in data:
#                 for cell in row:
#                     red, green, blue, a = cell
#                     black_areas = (red < 1) & (blue < 1) & (green < 1)
#                     cell = (0, 0, 0, 255)
            i = PIL.Image.fromarray(data)
            arr.append(i)
        return arr

speckle = SpeckleImage(probability = 1, threshold=5, corners_only=True)



#p = Augmentor.Pipeline(source_directory="../medium_cards/2ed", output_directory="../../data/validation/2ed")
p = Augmentor.Pipeline(source_directory="../aug_cards")
p.add_operation(speckle)
p.greyscale(probability=1)
# p.resize(probability=1, width=610, height=800, resample_filter=u'BICUBIC')
# p.zoom(probability=1, min_factor=0.55, max_factor=0.55)
# p.rotate_without_crop(probability=1, max_left_rotation=90, max_right_rotation=90)
# p.skew(probability=0.8, magnitude=0.15)
# p.zoom(probability=1, min_factor=0.5, max_factor=1)
# p.crop_by_size(probability=1, width=610, height=610, centre=True)
# p.random_brightness(probability=0.9, min_factor=0.6, max_factor=1.4)
# p.resize(probability=1, width=400, height=400, resample_filter=u'BICUBIC')


p.sample(1)



# g = p.keras_generator(batch_size=1)
# images, labels = next(g)

# print('images')
# print(images)
# print('labels')
# print(labels)
