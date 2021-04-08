import os
from loguru import logger
import sys
from datetime import datetime
import glob2
import pickle
import re
import string

def create_dir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            logger.info('Create directory: {}'.format(dir))
    except Exception as e:
        # use sys._getframe() -- it returns a frame object, whose attribute
        # f_code is a code object, whose attribute co_name is the name: this func name
        logger.error('[{}] : {}'.format(sys._getframe().f_code.co_name,e))
        exit(1)

def set_logger(folder_name):
    create_dir(folder_name)
    log_file_name = os.path.join(folder_name, '{:%Y%m%d}.log'.format(datetime.now().date()))
    logger.add(filename=log_file_name, encoding="utf8", format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | {message}')

def read_dir(dir):
    try:
        return glob2.glob(os.path.join(dir,'**','*.*'))
    except Exception as e:
        logger.error('[{}] : {}'.format(sys._getframe().f_code.co_name,e))
        exit(1)

def save_pickle(obj, file_name, folder):
    create_dir(folder)
    if file_name[-4:]=='.pkl':
        file_name = file_name[:-4]
    with open(os.path.join(folder,file_name + '.pkl'),'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_pickle(file_name, folder):
    file_name = file_name[:-4]
    if folder is not None:
        file_name = os.path.join(folder,file_name)
    with open(os.path.join(folder,file_name + '.pkl'),'rb') as f:
        return pickle.load(f)

def decontract_text(text):
    # specific
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can\'t", "can not", text)

    # general
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"n\u2019t", " not", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'s", " is", text)
    text = re.sub(r"\u2019s", " is", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'t", " not", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'m", " am", text)

    return text

def replace_emoticons(text,placeholder_pos = ' HAPPYEMOTICON ', placeholder_neg = ' SADEMOTICON '):
    emoticons_pos = [":)", ":-)", ":p", ":-p", ":P", ":-P", ":D", ":-D", ":]", ":-]", ";)", ";-)", ";p", ";-p", ";P",
                     ";-P", ";D", ";-D", ";]", ";-]", "=)", "=-)", "<3"]
    emoticons_neg = [":o", ":-o", ":O", ":-O", ":(", ":-(", ":c", ":-c", ":C", ":-C", ":[", ":-[", ":/", ":-/", ":\\",
                     ":-\\", ":n", ":-n", ":u", ":-u", "=(", "=-(", ":$", ":-$"]

    # replace positive emoticons by placeholder
    for e in emoticons_pos:
        text = text.replace(e, placeholder_pos)

    # replace negative emoticons by placeholder
    for e in emoticons_neg:
        text = text.replace(e, placeholder_neg)

    return text

def replace_emojis(text, placeholder_pos = ' HAPPYEMOJI ', placeholder_neg = ' SADEMOJI '):
    # define positive emojis
    emoji_pos = [u'\U0001f600', u'\U0001f601', u'\U0001f602', u'\U0001f923', u'\U0001f603', u'\U0001f604',
                 u'\U0001f605', u'\U0001f606',
                 u'\U0001f609', u'\U0001f60a', u'\U0001f60b', u'\U0001f60e', u'\U0001f60d', u'\U0001f618',
                 u'\U0001f617', u'\U0001f619',
                 u'\U0001f61a', u'\\U000263a', u'\U0001f642', u'\U0001f917']

    # define negative emojis
    emoji_neg = [u'\\U0002639', u'\U0001f641', u'\U0001f616', u'\U0001f61e', u'\U0001f61f', u'\U0001f624',
                 u'\U0001f622', u'\U0001f62d',
                 u'\U0001f626', u'\U0001f627', u'\U0001f628', u'\U0001f629', u'\U0001f62c', u'\U0001f630',
                 u'\U0001f631', u'\U0001f633',
                 u'\U0001f635', u'\U0001f621', u'\U0001f620', u'\U0001f612']

    # replace positive emojis by placeholder
    for e in emoji_pos:
        text = text.replace(e, placeholder_pos)

    # replace negative emojis by placeholder
    for e in emoji_neg:
        text = text.replace(e, placeholder_neg)

    return text

def replace_repeating_characters(text):
    #Replace repeating characters, for example, loveeeee into lovee - more than 2 of the same
    return re.sub(r'(.)\1{2,}', r'\1\1', text)

def replace_punctuation(text):
    for c in string.punctuation:
        text = text.replace(c, " ")

    return text

def replace_specific_characters(text):
    #Replace unwanted characters
    text = text.replace(u'\u201c', ' ')  # double opening quotes
    text = text.replace(u'\u201d', ' ')  # double closing quotes
    text = text.replace(u'\u2014', ' ')  # -
    text = text.replace(u'\u2013', ' ')  # -
    text = text.replace(u'\u2026', ' ')  # horizontal elipsses ...

    return text

def get_tokens(text):
    # split on whitespace
    tokens = text.split(" ")

    # remove space tokens and numbers, and convert to lowercase
    tokens = [x.lower() for x in tokens if x != " " and not x.isdigit()]

    return tokens

def clean_tweet(text):
    #replace new lines
    text = re.sub('\n',' ', text)
    # replace ampersand character
    text = text.replace('&amp;', ' and ')
    # replace @
    text = re.sub(r'@.*?( |$)', 'USERTAG ', text)
    # replace URL
    text = re.sub(r'http[s]{0,1}.*?( |$)', 'URLTAG ', text)
    # replace hashtag
    text = text.replace('#', '')
    # replace contractions
    text = decontract_text(text)
    # replace emoticons
    text = replace_emoticons(text)
    # replace emojis
    text = replace_emojis(text)
    # replace repeating charachtes : happyyyyy -> happyy
    text = replace_repeating_characters(text)
    # replace punctuation
    text = replace_punctuation(text)
    # replace specific characters
    text = replace_specific_characters(text)
    # replace double spaced
    text = text.replace("  ", " ").replace("  ", " ")
    # trim leading and trailing spaces
    text = text.strip()

    return text