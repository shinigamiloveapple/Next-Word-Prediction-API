
from keras.models import load_model
import numpy as np
import pickle
import heapq
import enchant

# Loading the variables to use it for the prediciton
with open('chars.pckl', 'rb') as fp:
    chars = pickle.load(fp)
    
    
char_index = np.load('char_index.npy',allow_pickle='TRUE').item()
index_char = np.load('index_char.npy',allow_pickle='TRUE').item()


# Loading model to test our prediction 
model = load_model('WTP_model.h5')
history = pickle.load(open('WTPhistory.p', 'rb'))


# Lets start prediction
    # To predict we will need some helper function.
    
seq_len = 40

def prepare_input(text):
    text = text.lower()
    x = np.zeros((1, seq_len, len(chars)))
    for t, char in enumerate(text):
        x[0, t, char_index[char]] = 1.
        
    return x


def sample(preds, top_n=3):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds)
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    
    return heapq.nlargest(top_n, range(len(preds)), preds.take)


def predict_completion(text):
    original_text = text
    completion = ''
    while True:
        x = prepare_input(text)
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, top_n=1)[0]
        next_char = index_char[next_index]
        text = text[1:] + next_char
        completion += next_char
        
        if len(original_text + completion) + 2 > len(original_text) and next_char == ' ':
            return completion



def predict_completions(text, n=3):
    x = prepare_input(text)
    preds = model.predict(x, verbose=0)[0]
    next_indices = sample(preds, n)
    return [index_char[idx] + predict_completion(text[1:] + index_char[idx]) for idx in next_indices]



def predict_from_list(quotes):
    d = enchant.Dict("en_US")  # This will check if the predicited word makes sense in english dictionary
    preds = {}
    for q in quotes:
        seq = q[-40:].lower()
        preds.setdefault(q,predict_completions(seq, 5))
    true_preds = {}
    for _key in preds.keys():
        comp_preds = []
        temp = []
        for _val in preds[_key]:
            string_pred = _key+_val
            string_pred = string_pred.strip().strip('.').strip(',').strip("'") # Removing ',' , '.', "'", and spaces.
            pred_tokens = string_pred.split()
            last_word =pred_tokens[-1]
            if d.check(last_word):
                req_str = ' '.join(pred_tokens) # Removing predicited words if that does not make a proper sense.
                if (req_str not in temp) and (req_str != _key):
                    temp.append(req_str)
                    comp_preds.append(req_str)
        true_preds.setdefault(_key,comp_preds)
    return true_preds

if __name__ == "__main__":
    quotes = [
        "It is not a lack of love, but a lack of friendship that makes unhappy marriages.",
        "That which does not kill us makes us stronger.",
        "I'm not upset that you lied to me, I'm upset that from now on I can't believe you.",
        "And those who were seen dancing were thought to be insane by those who could not hear the music.",
        "It is hard enough to remember my opinions, without also remembering my reasons for them!"
    ]

    print(predict_from_list(quotes))