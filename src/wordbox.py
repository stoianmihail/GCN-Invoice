from string import punctuation
import numpy as np
from src.featureCalculator import * 
from difflib import SequenceMatcher

kStripPunctuation = True

class_mapper = {'company' : 1, 'address' : 2, 'total' : 3, 'date' : 4, 'undefined' : 0}
inv_class_mapper = {1 : 'company', 2 : 'address', 3 : 'total', 4 : 'date', 0 : 'undefined'}

class Wordbox:
    def __init__(self, level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text):
        self.level = level
        self.page_num = page_num
        self.block_num = block_num
        self.par_num = par_num
        self.line_num = line_num
        self.word_num = word_num
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.conf = conf
        if not kStripPunctuation:
            self.text = text.strip()
        else:
            self.text = text.strip(punctuation).strip()
        self.neighs = {}
        
    def set_neighs(self, left=None, right=None, top=None, bottom=None):
        if left is not None:
            self.neighs['left'] = left
        if right is not None:
            self.neighs['right'] = right
        if top is not None:
            self.neighs['top'] = top
        if bottom is not None:
            self.neighs['bottom'] = bottom
        pass
        
    def set_feature_vector(self, feature_vector):
        self.feature_vector = feature_vector

    def similar(self, a, b, verbose=False):
        ret = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        if verbose:
          print(ret)
        return ret > 0.85

    def subsequences(self, orig_str, x, y):
      def local(fixed_len):
        return [orig_str[i : i + fixed_len] for i in range(len(orig_str) - fixed_len)]
      ret = []
      for l in range(max(x, 0), min(y + 1, len(orig_str))):
        ret += local(l)
      return ret

    def entail(self, source_text, target_text, verbose=False):
        if verbose:
          print(source_text + " vs " + target_text)
        if self.similar(source_text, target_text):
          return True
        for subseq in self.subsequences(target_text, len(source_text) - 1, len(source_text) + 1):
          if self.similar(source_text, subseq, verbose):
            return True
        return False

    def classify(self, parsed_json, verbose=False):
        # TODO: More than 1 class? Let user decide.
        self.class_number = class_mapper['undefined']
        for key in parsed_json:
            if self.entail(self.text, parsed_json[key], verbose) or self.entail(parsed_json[key], self.text, verbose):
              if verbose:
                print(self.text + ' chosen for ' + str(self.class_number))
              self.class_number = class_mapper[key]
              break
        pass
    def normalize(self, maxAbsDist):
    # Normalize the distance
        for key in self.neighs:
            self.neighs[key]['distance'] /= maxAbsDist

    def get_numeric_vector(self):
    # Get the numeric features
        def fetch(key):
            # TODO: is 0 a good default value?
            return self.neighs[key]['distance'] if key in self.neighs else 0
        # TODO: maybe change the order for better accuracy?
        return np.asarray([fetch('left'), fetch('top'), fetch('right'), fetch('bottom')])

    def get_boolean_vector(self):
        arr =  np.asarray([is_date(self.text), is_integer(self.text), is_price(self.text)])
        return arr.astype(int)

    def debug_class(self):
        return self.text + ' -> ' + inv_class_mapper[self.class_number]

    def __str__(self):
        def get_neigh(key):
            if key in self.neighs:
                return '(' + self.neighs[key]['which'].text + ', ' + str("{:.2f}".format(self.neighs[key]['distance'])) + ')'
            return '-'
        return 'text: ' + self.text + ' | l=' + get_neigh('left') + ' | r=' + get_neigh('right') + ' | t=' + get_neigh('top') + ' | b=' + get_neigh('bottom')