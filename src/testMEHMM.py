import pickle

f = open('../assets/MEHMModel.pickle','r')

(MEHMMEncoding, weights) = pickle.load(f)

print weights
