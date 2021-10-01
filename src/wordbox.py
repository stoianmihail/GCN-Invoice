from string import punctuation
kStripPunctuation = True

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
            self.text = text
        else:
            self.text = text.strip(punctuation)
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
        
    def normalize(self, maxAbsDist):
    # Normalize the distance
        for key in self.neighs:
            self.neighs[key]['distance'] /= maxAbsDist

    def __str__(self):
        def get_neigh(key):
            if key in self.neighs:
                return '(' + self.neighs[key]['which'].text + ', ' + str("{:.2f}".format(self.neighs[key]['distance'])) + ')'
            return '-'
        return 'text: ' + self.text + ' | l=' + get_neigh('left') + ' | r=' + get_neigh('right') + ' | t=' + get_neigh('top') + ' | b=' + get_neigh('bottom')