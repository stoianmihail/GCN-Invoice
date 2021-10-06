import numpy as np
from bpemb import BPEmb
from src.wordbox import Wordbox

kNumSubwords = 3
kDimension = 100
kVocabularySize = 2e6

def build_feature_vectors(boxes):
  # Construct word embeddings with a large vocabulary size.
  # Dismiss words with more than `kNumSubwords` subwords.
  #bpemb_en = state#
  bpemb_en = BPEmb(lang='en', dim=kDimension, vs=kVocabularySize)
  
  for box in boxes:
    vs = bpemb_en.embed(box.text)
    if vs.shape[0] > kNumSubwords:
      vs = vs[:kNumSubwords]
    #  print(box.text)
    #  # TODO: split with diff. width and left!
    #  # TODO: is this what we really want?
    #  # Dismiss
    #  embedding_vector = np.pad(np.asarray(vs[:kNumSubwords].flat), (0, kNumSubwords * kDimension - vs.shape[0] * vs.shape[1]), 'constant', constant_values=(0, 0))
    #  box.set_feature_vector(np.concatenate([embedding_vector, box.get_numeric_vector(), box.get_boolean_vector()]))
    #else:
    embedding_vector = np.pad(np.asarray(vs.flat), (0, kNumSubwords * kDimension - vs.shape[0] * vs.shape[1]), 'constant', constant_values=(0, 0))
    box.set_feature_vector(np.concatenate([embedding_vector, box.get_numeric_vector(), box.get_boolean_vector()]))
  return boxes