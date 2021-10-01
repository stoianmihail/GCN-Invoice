import cv2
import pytesseract
from pytesseract import Output
from src.wordbox import Wordbox
import re


kWidthThreshold = 2.0

"""
    remove words that only consist of special characters
"""
def isValid(text):
    if len(text.strip()) == 0:
        return False
    if re.match(r'[:;,.!?\\-]', text.strip()) is not None:
        return False
    return True

"""
    create a list of wordboxes found on the passed image
    TODO: use function to actually perform task1 and move the other stuff
"""
def task1(path, output_file=None):
    print('Process: ' + path)
    img = cv2.imread(path)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])

    wordboxes = []
    for i in range(n_boxes):
        if d['level'][i] == 5:
            wordboxes.append(Wordbox(d['level'][i], d['page_num'][i], d['block_num'][i], d['par_num'][i], d['line_num'][i], d['word_num'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i], d['conf'][i], d['text'][i]))

    for i in range(n_boxes):
        if d['level'][i] == 5:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])    
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    wordboxes = list(filter(lambda x: isValid(x.text), wordboxes))
    wordboxes = sorted(wordboxes, key=lambda x:(x.page_num, x.block_num, x.par_num, x.line_num, x.left))        

    curr_left, curr_top, curr_right, curr_bottom, curr_pos, curr_word = None, None, None, None, None, None

    ret = ''
    args = [-1] * 11 + [""]
    wordboxes.append(Wordbox(*args))
    new_wordboxes = []
    state = None
    curr_line_num = None
    acc_num_letters = 0
    acc_width = 0
    for wordbox in wordboxes:
        new_pos = (wordbox.page_num, wordbox.block_num, wordbox.par_num, wordbox.line_num)
        # Different? Then update the current line number and its state.
        if new_pos != curr_pos:
            acc_num_letters = 0
            acc_width = 0
            
        # Aggregate.
        acc_num_letters += len(wordbox.text.strip())
        acc_width += wordbox.width
            
        hasMerged = False
        if new_pos == curr_pos:
            # Computer the letter weight.
            letter_weight = acc_width / acc_num_letters
            
            # Should we merged?
            if (wordbox.left - curr_right) / letter_weight <= kWidthThreshold:
                curr_right = wordbox.left + wordbox.width
                curr_word = curr_word + ' ' + wordbox.text
                hasMerged = True
        # No, then create a new wordbox.
        if not hasMerged:
            if curr_pos is not None:
                assert state is not None
                if isValid(curr_word):
                    new_wordboxes.append(Wordbox(
                        6,
                        page_num=state['page_num'],
                        block_num=state['block_num'],
                        par_num=state['par_num'],
                        line_num=state['line_num'],
                        word_num=-1,
                        left=curr_left,
                        top=curr_top,
                        width=curr_right - curr_left,
                        height=curr_bottom - curr_top,
                        conf=-1,
                        text=curr_word
                    ))
            curr_word = wordbox.text
            curr_pos = new_pos
            curr_left = wordbox.left
            curr_top = wordbox.top
            curr_right = wordbox.left + wordbox.width
            curr_bottom = wordbox.top + wordbox.height
            
            # Update the state.
            state = {
                'page_num' : wordbox.page_num,
                'block_num' : wordbox.block_num,
                'par_num' : wordbox.par_num,
                'line_num' : wordbox.line_num
            }
    # Return the updated wordboxes.
    return new_wordboxes

