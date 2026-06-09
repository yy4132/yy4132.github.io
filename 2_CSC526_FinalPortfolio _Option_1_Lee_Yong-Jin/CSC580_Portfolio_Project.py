#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install tqdm


# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout, BatchNormalization, Activation, ZeroPadding2D, UpSampling2D, Conv2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
from tqdm import tqdm

# Load CIFAR10 data
(X, y), (_, _) = tf.keras.datasets.cifar10.load_data()

# Select a single class of images
X = X[y.flatten() == 8]

# Defining niput shape
image_shape = (32, 32, 3)
latent_dimensions = 100

# Utility function to build generator
def build_generator():
    model = Sequential()
    model.add(Dense(128 * 8 * 8, activation="relu", input_dim=latent_dimensions))
    model.add(Reshape((8, 8, 128)))
    model.add(UpSampling2D())
    model.add(Conv2D(128, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.78))
    model.add(Activation("relu"))
    model.add(UpSampling2D())
    model.add(Conv2D(64, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.78))
    model.add(Activation("relu"))
    model.add(Conv2D(3, kernel_size=3, padding="same"))
    model.add(Activation("tanh"))
    noise = Input(shape=(latent_dimensions,))
    image = model(noise)
    return Model(noise, image)

# Utility function to build discriminator
def build_discriminator():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=image_shape, padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
    model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
    model.add(BatchNormalization(momentum=0.82))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
    model.add(BatchNormalization(momentum=0.82))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    image = Input(shape=image_shape)
    validity = model(image)
    return Model(image, validity)

# Utility function to display generated images
def display_images(generator, epoch):
    r, c = 4, 4
    noise = np.random.normal(0, 1, (r * c, latent_dimensions))
    generated_images = generator.predict(noise)
    generated_images = 0.5 * generated_images + 0.5
    fig, axs = plt.subplots(r, c)
    count = 0
    for i in range(r):
        for j in range(c):
            axs[i, j].imshow(generated_images[count, :, :, :])
            axs[i, j].axis('off')
            count += 1
    plt.show()
    plt.close()

# Build and compile discriminator
discriminator = build_discriminator()
discriminator.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

# Make discriminator untrainable so generator can learn from fixed gradient
discriminator.trainable = False

# Build generator
generator = build_generator()

z = Input(shape=(latent_dimensions,))
image = generator(z)
valid = discriminator(image)

# Define combined model of generator and discriminator
combined_network = Model(z, valid)
combined_network.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

# Training parameters
num_epochs = 15000
batch_size = 32
display_interval = 2500

# Normalize input
X = (X / 127.5) - 1.

valid = np.ones((batch_size, 1))
valid += 0.05 * np.random.random(valid.shape)
fake = np.zeros((batch_size, 1))
fake += 0.05 * np.random.random(fake.shape)

losses = []

for epoch in tqdm(range(num_epochs), desc="Epochs"):
    index = np.random.randint(0, X.shape[0], batch_size)
    images = X[index]
    noise = np.random.normal(0, 1, (batch_size, latent_dimensions))
    generated_images = generator.predict(noise)
    
    discm_loss_real = discriminator.train_on_batch(images, valid)
    discm_loss_fake = discriminator.train_on_batch(generated_images, fake)
    discm_loss = 0.5 * np.add(discm_loss_real, discm_loss_fake)
    
    genr_loss = combined_network.train_on_batch(noise, fake)
    
    if epoch == 0 or epoch == num_epochs - 1:
        display_images(generator, epoch)
        if epoch == 0:
            plt.savefig('first_epoch_images.png')
        else:
            plt.savefig('last_epoch_images.png')
        plt.close()
    
    if epoch % display_interval == 0:
        display_images(generator, epoch)


# In[ ]:




