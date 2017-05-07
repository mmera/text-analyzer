from nltk.tokenize import sent_tokenize
import operator
import re
import sys
import io


def parse_S_contraction(prevWord):
    if re.match(r"([Ss]*[Hh]e$|[Ii]t$)", prevWord):
        return 'is'
    else:
        return '\'s'


def parse_contraction(prevWord, word):
    if word == 's':
        return parse_S_contraction(prevWord)
    else:
        return {
            'd': 'would',
            'll': 'will',
            'm': 'am',
            're': 'are',
            't': 'not',
            've': 'have'
        }.get(word, word)


def is_Contraction(word):
    return word in ['d', 'll', 'm', 're', 's', 't', 've']


def word_tokenize(text):
    return re.findall(r"\w+[\.-]\w+[\.-]?\w*|\d+,\d+|\d*\.\d+|[\w]+|[-.,!?;:&$()\"]", text)


def count_paragraphs(text):
    # RE finds gaps between paragraphs so add 1 to account for first paragraph
    return len(re.findall(r"(\n\n\w)", text)) + 1

def convert_contractions(word_list):
    for index, word in enumerate(word_list):
        try:
            if word_list[index + 1] == 't':
                word_list[index] = word[:-1]  # Hacks off the 'n'; doesn't work for "won't"
        except IndexError:
            pass
        if is_Contraction(word):
            prevWord = word_list[index - 1]
            word_list[index] = parse_contraction(prevWord, word)
    return word_list

def type_token_dict(word_list, count_flag='token'):
    token_count = {}
    type_count = {}
    # word_list = convert_contractions(word_list)
    for index, word in enumerate(word_list):
        if word not in token_count:
            token_count[word] = 1
            type_count[word.lower()] = 1

        else:
            token_count[word] += 1
            type_count[word.lower()] += 1

    if count_flag == 'token':
        return token_count
    elif count_flag == 'type':
        return type_count


def total_token_count(count_dictionary):
    return sum(count_dictionary.values())


def count_sentences(text):
    return len(sent_tokenize(text))


if __name__ == "__main__":

    file_to_read = sys.argv[1]
    file_to_write = sys.argv[2]

    f = io.open(file_to_read, "r", encoding="utf-8")
    text = f.read()
    sys.stdout = open(file_to_write, 'w')

    word_list = convert_contractions(word_tokenize(text))

    paragraph_count = count_paragraphs(text)
    token_count = type_token_count(word_list, 'token')
    type_count = type_token_count(word_list, 'type')
    total_count = total_vocab_count(token_count)

    sort_dict_by_count = sorted(
        token_count.items(), key=operator.itemgetter(1), reverse=True)

    print '# of paragraphs = ' + str(paragraph_count)
    print '# of sentences = ' + str(num_of_sentences(text))
    print '# of tokens: ' + str(total_count)
    print '# of types: ' + str(len(type_count))
    print '====================='

    for entry in sort_dict_by_count:
        print entry[0], entry[1]
