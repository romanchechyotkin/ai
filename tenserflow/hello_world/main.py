import tensorflow as tf

print(f"tenserflow version {tf.__version__}")

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("----------before scale----------")
print(x_train)

x_train, x_test = x_train / 255.0, x_test / 255.0

print("-----after scale--------")
print(x_train)


model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10),
])

