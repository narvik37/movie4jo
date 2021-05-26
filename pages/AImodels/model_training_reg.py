import random
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Dense, Flatten, Dropout
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from keras.utils import to_categorical
from keras.optimizers import SGD, Adam
from keras import callbacks
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras import metrics


def generate_dataset(N):
    X_data = pd.read_csv('ratings_genre.csv', usecols=['movieId', 'userAge', 'userGender', 'genre'])
    X = X_data.to_numpy(dtype='int32')

    y_data = pd.read_csv('ratings_genre.csv', usecols=['rating'])
    y = y_data.to_numpy(dtype='int32')

    X = X.reshape(N, 2, 2)
    y = y.reshape(N, 1)
    y = np.floor(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=True)

    return X_train, X_test, y_train, y_test


def train_model(X_train, X_test, y_train, y_test, num_dataset):
    train_num = int(num_dataset * 0.7)
    test_num = num_dataset - train_num

    X_train = X_train.reshape(train_num, 2, 2)
    X_test = X_test.reshape(test_num, 2, 2)

    # y_train = to_categorical(y_train, num_classes=6)
    # y_test = to_categorical(y_test, num_classes=6)

    model = Sequential([
        Input(shape=(2, 2), name='input_layer'),
        Conv1D(16, kernel_size=2, activation='sigmoid', padding='same', name='conv_layer1'),
        Conv1D(32, kernel_size=2, activation='relu', padding='same', name='conv_layer2'),
        Conv1D(32, kernel_size=2, activation='relu', padding='same', name='conv_layer3'),
        Dropout(0.5),
        Flatten(),
        Dense(100, activation='relu', name='hidden_layer1'),
        Dropout(0.5),
        Dense(20, activation='relu', name='hidden_layer2'),
        Dropout(0.5),
        Dense(1, activation='relu', name='output_layer')
    ])
    model.summary()
    model.compile(optimizer=Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-8),
                  loss='msle', metrics=['accuracy', 'recall'])

    earlystopping = callbacks.EarlyStopping(monitor="val_loss", mode="min", patience=5, restore_best_weights=True)

    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=500000, epochs=30, callbacks=[earlystopping])
    plot_loss_curve(history.history)

    model.save('model-02')

    return model


def plot_loss_curve(history):
    plt.figure()
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.show()

    print(history)
    print(f"train loss = {history['loss'][-1]}")
    print(f"validation loss = {history['val_loss'][-1]}")


if __name__ == '__main__':
    N = 8046382    # 속성 이름 row 제외한 데이터셋의 수

    X_train, X_test, y_train, y_test = generate_dataset(N)
    train_model(X_train, X_test, y_train, y_test, N)
