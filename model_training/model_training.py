import tensorflow as tf
from tensorflow import keras
from keras import layers
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from keras.models import load_model

def plt_show(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(50)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training accuracy")
    plt.plot(epochs_range, val_acc, label="Validation accuracy")
    plt.legend(loc='lower right')
    plt.title('Training and Validation accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training loss")
    plt.plot(epochs_range, val_loss, label="Validation loss")
    plt.legend(loc='upper right')
    plt.title('Training and Validation loss')
    
    plt.savefig('training.png')
    print("Training chart saved as 'training.png'")

train_dir = r"C:\Users\admin\Desktop\VSCProjects\CatDog\train"
validation_dir = r"C:\Users\admin\Desktop\VSCProjects\CatDog\validate"

IMG_SIZE = (180, 180)
BATCH_SIZE = 32

train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    shuffle = True,
    batch_size = BATCH_SIZE,
    image_size = IMG_SIZE
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    validation_dir,
    shuffle = False,
    batch_size = BATCH_SIZE,
    image_size = IMG_SIZE
)

# # This training gave us a model with ~87% val_accuracy and had ~0.32 val_loss
# data_augmentation = keras.Sequential(
#     [
#         layers.RandomFlip("horizontal", input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
#         layers.RandomRotation(0.1),
#         layers.RandomZoom(0.1),
#         layers.RandomTranslation(0.1, 0.1, fill_mode='reflect'),
#     ]
# )

# model = keras.Sequential([
#     data_augmentation,
#     layers.Rescaling(1./255),
#     layers.Conv2D(32, (3, 3), activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Conv2D(128, (3, 3), activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Flatten(),
#     layers.Dense(512, activation='relu'),
#     layers.Dropout(0.5),
#     layers.Dense(3, activation='softmax')
# ])

# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# model.summary()

# EPOCHS = 50
# es = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
# mc = tf.keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True, monitor='val_loss')
# history = model.fit(
#     train_dataset,
#     epochs=EPOCHS,
#     validation_data=validation_dataset,
#     callbacks=[es, mc]
# )
# plt_show(history)
# # ^^^^^^^^^^^^^^^^^^^^
# # now we will be fine tuning it

# model = load_model("best_model.h5") # ~90% val_accuracy, 0.29 val_loss
model = load_model(r"C:\Users\admin\Desktop\VSCProjects\CatDog\model_updated.keras") # ~92% val_accuracy, 0.2138 val_loss
model.summary()

new_optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

model.compile(
    optimizer = new_optimizer,
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
es = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, verbose=1)
mc = tf.keras.callbacks.ModelCheckpoint('CatDog/model_updated.keras', save_best_only=True, monitor="val_loss")

EPOCHS = 50
tuning_history = model.fit(
    train_dataset,
    epochs = EPOCHS,
    validation_data = validation_dataset,
    callbacks = [es, mc]
)

plt_show(tuning_history)