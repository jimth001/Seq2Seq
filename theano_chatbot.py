# -*- coding:utf-8 -*-
__author__ = 'chenjun'

from theano_models.seq2seq import Seq2SeqChatBot
from utils.chatbot_data_process import *


seed = 1234
rng = np.random.RandomState(seed)


def build_model(vocab_size=11394, hidden_size=128, layers_num=1, batch_size=100, n_epochs=5, evaluate=40):
    global rng
    encoder_inputs, decoder_inputs, decoder_target = load_train_data_for_theano("data/train_data.pkl")
    num_batchs = encoder_inputs.shape[0] // batch_size
    print ("train_batch_num: %d") % (num_batchs)
    model = Seq2SeqChatBot(rng, vocab_size, hidden_size, MAX_LENGTH, layers_num, learning_rate=0.01)
    epoch = 0
    while epoch < n_epochs:
        epoch += 1
        for batch_index in xrange(num_batchs):
            ei = encoder_inputs[batch_index * batch_size: (batch_index + 1) * batch_size]
            di = decoder_inputs[batch_index * batch_size: (batch_index + 1) * batch_size]
            dt = decoder_target[batch_index * batch_size: (batch_index + 1) * batch_size]
            em = get_mask(ei)
            dm = get_mask(di)
            loss = model.train(ei, em, di, dm, dt)
            if batch_index % 10 == 0:
                print ("epoch: %d/%d, batch: %d/%d, loss: %f") % (epoch, n_epochs, batch_index, num_batchs, loss)
    # evaluate
    for i in xrange(evaluate):
        index = np.random.randint(low=0, high=encoder_inputs.shape[0])
        ei = encoder_inputs[index]
        dt = decoder_target[index]
        em = get_mask(ei)
        generate = model.generate(ei, em)
        print "> ", indices2sentence(parse_output(ei), 'data/i2w.json')
        print "= ", indices2sentence(parse_output(dt), 'data/i2w.json')
        print "< ", indices2sentence(parse_output(generate), 'data/i2w.json')
        print ""


if __name__ == '__main__':
    build_model()