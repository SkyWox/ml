import numpy as np
import copy
from collections import deque
import keras
from keras.models import Model
from keras.layers import Flatten, Dense, Dropout


# Call this like:

model = None
callbacks = []


def makeModel():
    global model, callbacks
    if model != None:
        return
    inputs = keras.layers.Input(shape=(12, 4))

    output = Flatten()(inputs)
    output = Dense(100, activation='relu')(output)
    output = Dense(50, activation='relu')(output)
    output = Dense(20, activation='relu')(output)
    output = Dense(1, activation='relu', use_bias=False)(output)
    print(output)

    model = Model(inputs=inputs, outputs=output)

    tbCallBack = keras.callbacks.TensorBoard(
        log_dir='./log', histogram_freq=1, write_graph=True, write_images=True,
        embeddings_layer_names=None, embeddings_metadata=None, embeddings_freq=0)  # just had to remove embeddings_freq=1
    checkpointCallback = keras.callbacks.ModelCheckpoint(
        'model_running.h5', monitor='val_loss', verbose=0,
        save_best_only=True, save_weights_only=False, mode='auto', period=1)
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.2,
        patience=5, min_lr=0.0001)
    callbacks = [tbCallBack, checkpointCallback, reduce_lr]

    model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.001))
    from keras.models import load_model
    # model = load_weights('model_running.h5')


all_tricks = []
whowon = []

suits = ['hrt', 'dia', 'spd', 'clb']
# ace is high so = 15
deck = [suit + str(num) for num in range(2, 14)
        for suit in ['hrt', 'dia', 'spd', 'clb']]
deck2D = np.ones((4, 13), dtype=np.int)
current_deck = list(deck)
goes_first = 0
hands = []
scores = np.zeros(4)


def train():
    global model, boardgames, whowon
    makeModel()
    # print("Boardgames is:", np.array(boardgames).shape, "whowon:", np.array(whowon).shape)
    model.fit(np.array(all_tricks), np.array(whowon), epochs=10, validation_split=0.2, shuffle=True,
              verbose=0, callbacks=callbacks)


# board[0,:,:] is for computer player.  0 if there's no piece and 1 if there is
# board[1,:,:] is for other player.     0 if there's no piece and 1 if there is
current_game_boards = []


def ai_best_card(trick, suit, player):
    global model
    makeModel()
    hand = valid_cards(trick, suit)

    if len(hand) > 0:
        best_x = 0
        best_prob_to_win = 0
        for x in range(len(hand)):
            prob_to_win = model.predict(
                np.array([trick]), batch_size=1, verbose=0)[0]
            if prob_to_win > best_prob_to_win:
                best_x = x
                best_prob_to_win = prob_to_win
        return hand[best_x]
    else:
        print('Player %d is out' % player)
        return 'nul0'


def shuffle_deal():
    global current_deck, hands, goes_first
    current_deck = list(deck)
    np.random.shuffle(current_deck)
    d = deque(current_deck)
    hands = [current_deck[i::4] for i in range(0, 4)]
    x = [x for x in hands if 'clb2' in x][0]
    goes_first = hands.index(x)


def find(lst, predicate):
    return next((i for i, j in enumerate(lst) if predicate(j)), -1)


def play_trick():
    trick2 = []
    trick = ['nul0', 'nul0', 'nul0', 'nul0']
    suit = ''
    if hands[goes_first].count('clb2') == 1:
        # move 2 of clubs to front of hand
        hands[goes_first].insert(0, hands[goes_first].pop(
            hands[goes_first].index('clb2')))

    player = goes_first
    for i in range(4):
        if i == 1:
            trick_set = list(set(trick))
            trick_set.pop(trick_set.index('nul0'))
            suit = trick_set[0][:3]

        if player == 1:
            chosen_card = ai_best_card(trick, player, suit)
        else:
            chosen_card = pick_card(player, suit)
        trick[player] = chosen_card
        hands[player].pop(hands[player].index(chosen_card))
        if i == 0:
            print('Player %d goes first, playing ' % player + trick[player])
        if player < 3:
            player = player + 1
        else:
            player = 0

    print(trick)
    winner_collects(trick)


def valid_cards(hand, suit):
    valid_hand = list(hand)
    for card in hand:
        if card[:3] != suit:
            valid_hand.pop(valid_hand.index(card))
    if len(valid_hand) == 0:
        return hand
    return valid_hand


def pick_card(player, suit):
    if suit == '':
        return hands[player][0]
    if len(hands[player]) > 0:
        return valid_cards(hands[player], suit)[0]
    else:
        return 'nul0'
        print('Player %d is out' % player)


def remove_suit(a):
    return int(a[3:])


def winner_collects(trick):
    global scores, goes_first
    winner = np.argmax([remove_suit(a) for a in trick])
    original_score = scores[winner]
    for i in trick:
        if i == 'spd12':
            scores[winner] += 13
        if i[:3] == 'hrt':
            scores[winner] += 1

    print('Player %d now has %d points' % (winner, scores[winner]))
    all_tricks.append(trick)
    winner_list = np.zeros(4)
    winner_list[winner] = scores[winner] - original_score
    whowon.append(winner_list)
    goes_first = winner


def get_random_move(hand, suit):
    valid_card = valid_cards(hand, suit)
    return valid_card[np.random.randint(len(valid_card))]


def cardDemo():
    shuffle_deal()

    for i in range(12):
        play_trick()
    print('Final scores:')
    print(scores)
    print('Who won list:')
    # train()
    print([y for x in np.array(whowon) for y in x])
    print([y for x in np.array(all_tricks) for y in x])


if __name__ == "__main__":
    print("Hello!")
    # playAgainstSelfRandomly()
    cardDemo()
