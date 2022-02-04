from tensorflow.keras.layers import Input, Flatten, Dense, Dropout, Conv2D, MaxPool2D, Rescaling
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import SparseCategoricalCrossentropy


def get_model(img_height, img_width, num_classes):
    model = Sequential([
        Input((img_height, img_width, 1)),
        # Normalization layer for converting inputs to [0, 1] floats
        Rescaling(1. / 255),
        Conv2D(8, kernel_size=(5, 5), activation='relu', input_shape=(img_height, img_width, 1)),
        MaxPool2D(pool_size=(2, 2)),
        Conv2D(8, kernel_size=(7, 7), activation='relu'),
        MaxPool2D(pool_size=(2, 2)),
        Conv2D(8, kernel_size=(5, 5), activation='relu'),
        Conv2D(8, kernel_size=(7, 7), activation='relu'),
        MaxPool2D(pool_size=(2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax'),
    ])

    model.compile(optimizer='adam',
                  loss=SparseCategoricalCrossentropy(),
                  metrics=['accuracy']
                  )

    return model
