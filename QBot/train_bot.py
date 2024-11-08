import os

import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Concatenate, Flatten
from tensorflow.keras import Model

from QBot.Environments.SimulatedEnvironment import SimulatedEnvironment
from QBot.Environments.States.EnemyState import EnemyState
from QBot.Environments.States.PlayerState import PlayerState

NUM_ACTIONS = 10


def create_deep_q_model(deck_input_dim, state_input_dim, deck_embed_dim=32) -> tf.keras.Model:
    deck_input = Input(shape=(deck_input_dim,), name='deck_input')


    deck_embedding = Embedding(input_dim=PlayerState.NUM_UNIQUE_CARDS, output_dim=deck_embed_dim)(deck_input)
    deck_embedding_flat = Flatten()(deck_embedding)

    state_input = Input(shape=(state_input_dim,), name='state_input')

    concatenated = Concatenate()([deck_embedding_flat, state_input])

    dense_1 = Dense(128, activation='relu')(concatenated)
    dense_2 = Dense(64, activation='relu')(dense_1)

    output = Dense(NUM_ACTIONS, activation='linear', name='output')(dense_2)

    model = Model(inputs=[deck_input, state_input], outputs=output)
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


def main():
    state_input_dim = PlayerState.get_len()[1] + EnemyState.get_len()*3
    model: Model = create_deep_q_model(PlayerState.get_len()[0], state_input_dim)
    target_model = create_deep_q_model(PlayerState.get_len()[0], state_input_dim)
    target_model.set_weights(model.get_weights())
    env = SimulatedEnvironment(model, target_model, path_to_sim=os.path.join(os.path.curdir, "..", "CombatSim"))
    env.train_model(10)


if __name__ == '__main__':
    main()
