from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import Augmentor

from augmentor import SpeckleImage, SharpCorners

speckle_image = SpeckleImage(probability = 1)
sharp_corners = SharpCorners(probability = 1)

img_width, img_height = 400, 400

train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 2285
nb_validation_samples = 283
epochs = 50
batch_size = 32

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.1))
model.add(Dense(1))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

p = Augmentor.Pipeline(source_directory="../train")
p.add_operation(sharp_corners)
p.random_brightness(probability=0.9, min_factor=0.65, max_factor=1.4)
p.resize(probability=1, width=610, height=800, resample_filter=u'BICUBIC')
p.zoom(probability=1, min_factor=0.55, max_factor=0.55)
p.rotate_without_crop(probability=1, max_left_rotation=90, max_right_rotation=90)
p.skew(probability=0.8, magnitude=0.15)
p.zoom(probability=1, min_factor=0.5, max_factor=1)
p.crop_by_size(probability=1, width=610, height=610, centre=True)
p.resize(probability=0.5, width=300, height=300, resample_filter=u'BILINEAR')
p.resize(probability=1, width=400, height=400, resample_filter=u'BICUBIC')
p.greyscale(probability=1)
p.add_operation(speckle_image)
g_train = p.keras_generator(batch_size=batch_size)

q = Augmentor.Pipeline(source_directory="../validate")
q.add_operation(sharp_corners)
q.random_brightness(probability=0.9, min_factor=0.65, max_factor=1.4)
q.resize(probability=1, width=610, height=800, resample_filter=u'BICUBIC')
q.zoom(probability=1, min_factor=0.55, max_factor=0.55)
q.rotate_without_crop(probability=1, max_left_rotation=90, max_right_rotation=90)
q.skew(probability=0.8, magnitude=0.15)
q.zoom(probability=1, min_factor=0.5, max_factor=1)
q.crop_by_size(probability=1, width=610, height=610, centre=True)
q.resize(probability=0.5, width=300, height=300, resample_filter=u'BILINEAR')
q.resize(probability=1, width=400, height=400, resample_filter=u'BICUBIC')
q.greyscale(probability=1)
q.add_operation(speckle_image)
g_validate = q.keras_generator(batch_size=batch_size)

model.fit_generator(
    g_train,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=g_validate,
    validation_steps=nb_validation_samples // batch_size)

model.save_weights('first_real.h5')
model.save('mtg-model-real.h5')