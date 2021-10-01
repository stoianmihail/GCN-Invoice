import cv2
from numpy import heaviside
from src.wordbox import Wordbox
from src.task1 import task1

def gravityCenter(box):
# Compute the gravity center of `box`.
    return (box.left + box.width / 2, box.top + box.height / 2)

def isHorizontal(this, other):
# Check whether `other` is placed horizontally wrt to `this`.
    if this.top >= other.top + other.height:
        return False
    if other.top >= this.top + this.height:
        return False
    return True

def isVertical(this, other):
# Check whether `other` is placed vertically wrt to `this`.
    if this.left >= other.left + other.width:
        return False
    if other.left >= this.left + this.width:
        return False
    return True

def coordDiff(this, other, axis):
# Coordinate difference on `axis`.
    return abs(gravityCenter(this)[axis] - gravityCenter(other)[axis])

def isHCloser(this, other, that):
# Is `other` horizontally closer than `that` wrt `this`?
    return coordDiff(this, other, 0) <= coordDiff(this, that, 0) 

def isVCloser(this, other, that):
# Is `other` vertically closer than `that` wrt `this`?
    return coordDiff(this, other, 1) <= coordDiff(this, that, 1) 

def isLeft(this, other):
# Left?
    return isHorizontal(this, other) and gravityCenter(this)[0] >= gravityCenter(other)[0]

def isRight(this, other):
# Right?
    return isHorizontal(this, other) and gravityCenter(this)[0] <= gravityCenter(other)[0]

def isTop(this, other):
# Top?
    return isVertical(this, other) and gravityCenter(this)[1] >= gravityCenter(other)[1]

def isBottom(this, other):
# Bottom?
    return isVertical(this, other) and gravityCenter(this)[1] <= gravityCenter(other)[1]

# Function mapper.
mapper = {'left': {'direction_fn' : isLeft, 'closer_fn' : isHCloser},
          'right' : {'direction_fn' : isRight, 'closer_fn' : isHCloser},
          'top' : {'direction_fn' : isTop, 'closer_fn' : isVCloser},
          'bottom' : {'direction_fn' : isBottom, 'closer_fn' : isVCloser}
         }

def computeDistance(direction, this, other, h, w):
    # Note: `left` and `top` are negative while `right` and `bottom` are positive.
    if direction == 'left':
        return ((other.left + other.width) - this.left) / w
    elif direction == 'right':
        return (other.left - (this.left + this.width)) / w
    elif direction == 'top':
        return ((other.top + other.height) - this.top) / h
    else: # bottom:
        return (other.top - (this.top + this.height)) / h
    # Unreachable
    return 0

# Update the neighbors.
def update(coord, this, other, h, w):
    for key in coord.keys():
        if mapper[key]['direction_fn'](this, other):
            if (coord[key] is None) or (mapper[key]['closer_fn'](this, other, coord[key]['which'])):
                coord[key] = {'which' : other, 'distance' : computeDistance(key, this, other, h, w)}

def cmpMaxAbsDist(curr, coord):
# Update the maximum absolute distance (needed for distance normalization)
    for key in coord:
        if coord[key] is not None:
            curr = abs(max(curr, coord[key]['distance']))
    return curr

def construct_graph(filepath):
# Construct the graph.
    # Fetch the boxes
    boxes = task1(filepath)
    
    # TODO: multi-page invoices? Take `h` and `w` for each page separately (to compute edge costs)
    img = cv2.imread(filepath)
    (h, w) = img.shape[:2]

    # Compute edge costs.
    maxAbsDist = 0
    for i, box1 in enumerate(boxes):
        coord = {'left' : None, 'right' : None, 'top' : None, 'bottom' : None}
        for j, box2 in enumerate(boxes):
            if i == j:
                continue
            update(coord, box1, box2, h, w)
        # Set the neighbors.
        box1.set_neighs(left=coord['left'], right=coord['right'], top=coord['top'], bottom=coord['bottom'])

        # Compute the maximum absolute distance.
        maxAbsDist = cmpMaxAbsDist(maxAbsDist, coord)
    # And normalize the boxes.
    for box in boxes:
        box.normalize(maxAbsDist)
    return boxes