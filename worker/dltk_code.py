# TF_CONFIG={\"cluster\": {\"worker\": [\"worker1:12345\", \"worker2:12345\"]}, \"task\": {\"index\": 0, \"type\": \"worker\"}}"

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD
import numpy as np
import logging

#logging.info("1111111111111111111111111")

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(
    tf.distribute.experimental.CollectiveCommunication.AUTO,
)

#logging.info("222222222222222222222222222")

with strategy.scope():

    model = Sequential()
    model.add(Dense(8, input_dim=2))
    model.add(Activation('tanh'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    sgd = SGD(lr=0.1)
    model.compile(loss='binary_crossentropy', optimizer=sgd)

#logging.info("333333333333333333333333333")


def fit(events):
    logging.info("4444444444444444444444")

    input_tensors = np.array([
        [
            int(e["i1"]),
            int(e["i2"]),
        ] for e in events
    ])
    output_tensors = np.array([
        [
            int(e["o"]),
        ] for e in events
    ])
    tensors = (input_tensors, output_tensors)
    train_dataset = tf.data.Dataset.from_tensor_slices(tensors)
    train_dataset = train_dataset.batch(
        64 * strategy.num_replicas_in_sync,
        # drop_remainder=True,
    )
    #options = tf.data.Options()
    #options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
    #train_dataset = train_dataset.with_options(options)
    #logging.info("5555555555555555555555555")
    model.fit(train_dataset, steps_per_epoch=1, epochs=1)
    #logging.info("6666666666666666666666666666")
    return []


# if hostname == "worker1":
#    results = [
#        model.predict_proba([[1, 1]]),
#        model.predict_proba([[0, 0]]),
#        model.predict_proba([[1, 0]]),
#        model.predict_proba([[0, 1]])
#    ]
#    print(results)
