import Augmentor
from Augmentor.Operations import Operation
import PIL
from PIL import Image
import numpy as np
import random
np.set_printoptions(threshold=np.nan)

# Create your new operation by inheriting from the Operation superclass:
class FoldImage(Operation):
    # Here you can accept as many custom parameters as required:
    def __init__(self, probability):
        # Call the superclass's constructor (meaning you must
        # supply a probability value):
        Operation.__init__(self, probability)

    # Your class must implement the perform_operation method:
    def perform_operation(self, image):
        # Start of code to perform custom image operation.
        print('fold')
        #
        data = np.array(image[0]).astype('uint8')
        data = PIL.Image.fromarray(data)

        # im = Image.open(data)

        im = data.convert('RGBA')

        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, a = data.T # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        white_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed

        im2 = Image.fromarray(data)
        im2.show()
        # End of code to perform custom image operation.
        # Return the image so that it can further processed in the pipeline:
        image = PIL.Image.fromarray(data)
        return image

fold = FoldImage(probability = 1)



#p = Augmentor.Pipeline(source_directory="../medium_cards/2ed", output_directory="../../data/validation/2ed")
p = Augmentor.Pipeline(source_directory="../aug_cards")
p.add_operation(fold)
p.greyscale(probability=1)
p.resize(probability=1, width=610, height=800, resample_filter=u'BICUBIC')
p.zoom(probability=1, min_factor=0.55, max_factor=0.55)
p.rotate_without_crop(probability=1, max_left_rotation=90, max_right_rotation=90)
p.skew(probability=0.8, magnitude=0.15)
p.zoom(probability=1, min_factor=0.5, max_factor=1)
p.crop_by_size(probability=1, width=610, height=610, centre=True)
p.random_brightness(probability=0.9, min_factor=0.6, max_factor=1.4)
p.resize(probability=1, width=400, height=400, resample_filter=u'BICUBIC')


p.sample(1)



g = p.keras_generator(batch_size=1)
images, labels = next(g)

# print('images')
# print(images)
# print('labels')
# print(labels)

# im, labels = next(g)
# print('images')
# print(images)
# print('labels')
# print(labels)

#data = np.array(images[0]).astype('uint8')

    # Perform your custom operations here
#print(data)
#image = PIL.Image.fromarray(data)
#print(image)
# im = Image.open('../aug_cards/2ed_40_Serra Angel.jpg')
#im = image.convert('RGBA')

# data = np.array(im)

# red, green, blue = data.T

# white_areas = (red == 0) & (blue == 0) & (green == 0)

# below replacing with SAME random number each time.  not optimal.
# data[..., :-1][white_areas.T] = (random.randint(1,256), random.randint(1,256), random.randint(1,256))

#im2 = Image.fromarray(data)
#im2.show()

