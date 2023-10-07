import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Conv2D, MaxPool2D, Dropout, Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.callbacks import LearningRateScheduler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle


def preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.equalizeHist(image)
    image = image / 255.0
    image = image.astype("float32")
    return image


def create_model(input_shape, output_shape):
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(MaxPool2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(output_shape, activation="softmax"))
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def scheduler(epoch, lr):
    if epoch < 15:
        return lr
    else:
        return lr * tf.math.exp(-0.1)


PATH = "../images"
BATCH_SIZE = 64
EPOCHS = 32

images = []
classNumber = []
digits = os.listdir(PATH)

numClasses = len(digits)
for i in range(1, numClasses + 1):
    num_list = os.listdir(PATH + "/digit-" + str(i))
    for j in num_list:
        currImage = cv2.imread(PATH + "/digit-" + str(i) + "/" + j)
        currImage = cv2.resize(currImage, (32, 32), cv2.INTER_AREA)
        images.append(currImage)
        classNumber.append(i)

images = np.array(images)
classNumber = np.array(classNumber)

x_train, x_test, y_train, y_test = train_test_split(
    images, classNumber, test_size=0.2, random_state=123
)
encoder = LabelEncoder()
encoder.fit(y_train)
y_train, y_test = encoder.transform(y_train), encoder.transform(y_test)
y_train, y_test = (
    to_categorical(y_train, numClasses),
    to_categorical(y_test, numClasses),
)

x_train = np.array(list(map(preprocess, x_train)))
x_test = np.array(list(map(preprocess, x_test)))

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

data_gen = ImageDataGenerator(
    width_shift_range=0.1, height_shift_range=0.1, zoom_range=0.2, shear_range=0.1
)

lrcallback = LearningRateScheduler(scheduler)

model = create_model(
    input_shape=(x_train.shape[1], x_train.shape[2], 1), output_shape=numClasses
)

r = model.fit(
    data_gen.flow(x_train, y_train, batch_size=BATCH_SIZE, shuffle=True),
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    steps_per_epoch=x_train.shape[0] // BATCH_SIZE,
    validation_data=data_gen.flow(x_test, y_test, batch_size=BATCH_SIZE),
    validation_steps=x_test.shape[0] // BATCH_SIZE,
    callbacks=[lrcallback],
)

model.save("digit_ocr.h5")
