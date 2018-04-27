from utilities import read_file, write_file
from cebstemmer import stemmer
from nltk.corpus import words as english_words
import string


'''
Tokenize the sentences
'''
def tokenize():
    sentences = read_file('data/sentences.txt', strip=True)

    tokens = []
    english_corpus = english_words.words()

    for idx, sentence in enumerate(sentences):
        print(idx)
        sentence = sentence.replace(',', '')
        sentence = sentence.replace('(', '')
        sentence = sentence.replace(')', '')
        sentence = sentence.replace('.', '')
        sentence = sentence.replace(':', '')

        words = sentence.split(' ')

        for idx, word in enumerate(words):
            word = word.decode('utf-8')
            word = filter(lambda x: x in string.printable, word)
            if idx > 0:
                if not word.istitle() and not word.isupper() and not word.isdigit() and word.lower() not in english_corpus:
                    word = word.lower()
                    if word not in tokens:
                        tokens.append(word)
            else:
                word = word.lower()
                if word not in tokens:
                    tokens.append(word)

    write_file(name='data/input_tokens.txt', contents=tokens, no_encode=True, append_newline=True, add_newline=False)

'''
Feeds the input tokens in stemmer
The output is: word, root word, prefix, infix, suffix, dictionary_entry
'''
def stem_tokens():
    tokens = read_file('data/input_tokens.txt', strip=True)
    output = []
    for idx, token in enumerate(tokens):
        print(idx)
        stem = stem_word(word=token)
        affix = str(stem.prefix) + ' ' + str(stem.infix) + ' ' + str(stem.suffix)
        is_entry = 1 if stem.is_entry else 0
        output.append(stem.word + ' ' + stem.root + ' ' + affix + ' ' + str(is_entry))

    write_file(name='data/output_tokens-nc.txt', contents=output, no_encode=True, append_newline=True, add_newline=False)

'''
Formats the output tokens to dict
'''
def to_panda_data():
    output = read_file('data/output_tokens.txt', strip=True)
    panda_data = []
    indexes = []
    for o in output:
        data = {}
        o = o.split(' ')
        indexes.append(o[0])
        data['root'] = o[1]

        data['is_root'] = o[0] == o[1]
        if o[2] != 'None':
            data['prefix'] = o[2]

        if o[3] != 'None':
            data['infix'] = o[3]

        if o[4] != 'None':
            data['suffix'] = o[4]

        data['is_entry'] = True if int(o[5]) == 1 else False

        if len(o) == 7:
            data['is_valid'] = True if int(o[6]) == 1 else False
        else:
            data['is_valid'] = 'Null'
        panda_data.append(data)

    return {
     'data': panda_data,
     'index': indexes
    }


def statistics(df=None):
    stats = []
    
    stats.append(df.count()['is_valid'])
    stats.append(df[(df.is_valid == True)].count()['is_valid'])
    stats.append(df[(df.is_valid == False)].count()['is_valid'])
    stats.append((df[(df.is_valid == True)].count()['is_valid'] / float(df.count()['is_valid'])) * 100)
    stats.append(df[(df.is_entry == True)].count()['is_entry'])
    stats.append(df[(df.is_entry == True) & (df.is_valid == True)].count()['is_entry'])
    stats.append(df[(df.is_entry == True) & (df.is_valid == False)].count()['is_entry'])
    stats.append(df[(df.is_entry == False)].count()['is_entry'])
    stats.append(df[(df.is_entry == False) & (df.is_valid == True)].count()['is_entry'])
    stats.append(df[(df.is_entry == False) & (df.is_valid == False)].count()['is_entry'])

    indices = [
        'Tokens',
        'Correct Root',
        'Incorrect Root',
        'Correct Root %',
        'Found Tokens',
        'Correct Root (Found)',
        'Incorrect Root (Found)',
        'Unknown Tokens',
        'Correct Root (Unknown)',
        'Incorrect Root (Unknown)'
    ]

    return {
        'values': stats,
        'index': indices
    }
if __name__ == '__main__':
    # tokenize()
    # stem_tokens()
    pass