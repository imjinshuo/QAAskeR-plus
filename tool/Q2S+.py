import argparse
import spacy
import numpy as np
from nltk import Tree
from tqdm import tqdm
from pycorenlp import StanfordCoreNLP
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer

nlp_spacy = spacy.load('en_core_web_sm')


def read_tree(tree):
    if isinstance(tree, str):
        return tree
    else:
        return [read_tree(i) for i in tree]


def generate(question):
    source_question_doc = nlp_spacy(question)
    texts = [token.text for token in source_question_doc]
    poses = [token.pos_ for token in source_question_doc]
    tags = [token.tag_ for token in source_question_doc]
    deps = [token.dep_ for token in source_question_doc]
    lemmas = [token.lemma_ for token in source_question_doc]
    if texts[0] not in ['what', 'What', 'where', 'Where', 'who', 'Who',
                        'when', 'When', 'which', 'Which', 'whose', 'Whose']:
        raise
    WH_index = 0
    WH_word = lemmas[WH_index]
    WH2type = {'what':'thing', 'which':'thing', 'when':'time', 'who':'person', 'whose':"person's", 'where':'location',
               'What':'thing', 'Which':'thing', 'When':'time', 'Who':'person', 'Whose':"person's", 'Where':'location'}
    ROOT_index = deps.index('ROOT')
    if deps[WH_index+1] == 'aux':
        aux_index = deps.index('aux')
        if lemmas[aux_index] in ['do', 'have', 'be']:
            substitute_part = ['the', WH2type[WH_word]]
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[aux_index + 1:-1])
            else:
                substitute_part.extend(texts[aux_index + 1:])
        elif poses[deps.index('aux') + 1] in ['DET', 'ADJ', 'NOUN']:
            raise
        else:
            substitute_part = ['the', WH2type[WH_word]]
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[aux_index:-1])
            else:
                substitute_part.extend(texts[aux_index:])
    elif 'aux' in deps and 'VERB' not in poses[:deps.index('aux')]:
        if lemmas[deps.index('aux')] in ['do', 'have', 'be']:
            aux_index = deps.index('aux')
            the_thing = texts[1:aux_index]
            substitute_part = ['the']
            substitute_part.extend(the_thing)
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[aux_index + 1:-1])
            else:
                substitute_part.extend(texts[aux_index + 1:])
        elif poses[deps.index('aux') + 1] in ['DET', 'ADJ', 'NOUN']:
            raise
        else:
            aux_index = deps.index('aux')
            the_thing = texts[1:aux_index]
            substitute_part = ['the']
            substitute_part.extend(the_thing)
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[aux_index + 1:-1])
            else:
                substitute_part.extend(texts[aux_index + 1:])
    elif poses[1] not in ['AUX', 'VERB']:
        the_thing = texts[1:ROOT_index]
        if lemmas[ROOT_index] == 'be':
            substitute_part = ['the']
            substitute_part.extend(the_thing)
            substitute_part.append('that')
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[ROOT_index:-1])
            else:
                substitute_part.extend(texts[ROOT_index:])
        else:
            substitute_part = ['the']
            substitute_part.extend(the_thing)
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[ROOT_index:-1])
            else:
                substitute_part.extend(texts[ROOT_index:])
    else:
        if lemmas[ROOT_index] == 'be':
            if lemmas[ROOT_index+1] == 'not':
                substitute_part = ['the', WH2type[WH_word]]
                substitute_part.append('that')
                if poses[-1] == 'PUNCT':
                    substitute_part.extend(texts[ROOT_index:-1])
                else:
                    substitute_part.extend(texts[ROOT_index:])
            else:
                substitute_part = []
                if poses[-1] == 'PUNCT':
                    substitute_part.extend(texts[ROOT_index+1:-1])
                else:
                    substitute_part.extend(texts[ROOT_index+1:])
        else:
            substitute_part = ['the', WH2type[WH_word]]
            if poses[-1] == 'PUNCT':
                substitute_part.extend(texts[ROOT_index:-1])
            else:
                substitute_part.extend(texts[ROOT_index:])
    return substitute_part




def index_output(texts, this_output):
    this_output_doc = nlp_spacy(this_output)
    this_output_text = [token.text for token in this_output_doc]
    for index in range(0, len(texts)-len(this_output_text)+1):
        if texts[index:index+len(this_output_text)] == this_output_text:
            return [index, index+len(this_output_text)]
    return [0, 0]


def main():
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--npy_file_path",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--out_file_path",
        default=None,
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()
    npy_info = np.load(npy_file_path, allow_pickle=True)
    npy_info = npy_info.tolist()

    output = []
    all_question = []
    all_GT = []
    all_article = []
    dataset = ""
    for i in npy_info:
        output.append(i[1])
        all_question.append(i[0])
        all_GT.append(i[5])
        all_article.append(i[2])
        dataset = i[4]
    all_output = []
    for index in tqdm(range(len(all_article))):
        this_output = output[index]
        this_question = all_question[index]
        this_GT = all_GT[index]
        this_article = all_article[index]
        this_article_doc = nlp_spacy(this_article)
        try:
            substitute_part = generate(this_question)
            substitute_text = TreebankWordDetokenizer().detokenize(substitute_part)
        except:
            continue
        if_first = True
        this_question_doc = nlp_spacy(this_question)
        this_question_noun_list = [token.lemma_ for token in this_question_doc if token.pos_ == 'NOUN']
        this_output_doc = nlp_spacy(this_output)
        this_output_lemma = [token.lemma_ for token in this_output_doc]
        this_output_pos = [token.pos_ for token in this_output_doc]
        if 'NOUN' not in this_output_pos:
            continue
        for sentence in this_article_doc.sents:
            if if_first:
                if_first = False
                continue
            this_sentence_text = sentence.text
            if ',' in this_sentence_text or ';' in this_sentence_text:
                continue
            if this_output in this_sentence_text:
                try:
                    this_sentence_pos = [token.pos_ for token in sentence]
                    this_sentence_lemma = [token.lemma_ for token in sentence]
                    if_same_knowldege = True
                    for NOUN in this_question_noun_list:
                        if NOUN not in this_sentence_lemma:
                            if_same_knowldege = False
                            break
                    if if_same_knowldege:
                        continue
                    if 'VERB' in this_sentence_pos or 'AUX' in this_sentence_pos:
                        all_output.append({'statement': str(this_sentence_text),
                                           'answer': this_output,
                                           'article': this_article,
                                           'question': this_question,
                                           'GT': this_GT,
                                           'index': index,
                                           'dataset': dataset,
                                           'subst_text':substitute_text})
                except:
                    continue
    np.save(args.out_file_path, all_output)



if __name__ == "__main__":
    main()