import argparse
import random
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
import spacy
import re
import os
import json
import csv
from nltk.tokenize.treebank import TreebankWordDetokenizer

nlp = spacy.load("en_core_web_sm")
SPARQLPATH = "http://localhost:8890/sparql"


def SQL_MID2property(mid):
    property = list()
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery("""PREFIX ns: <http://rdf.freebase.com/ns/> SELECT distinct ?p WHERE {ns:%s ?p [].}""" % (mid))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        for binding in results['results']['bindings']:
            property.append(binding['p']['value'][27:])
    except:
        pass
    return property


def SQL_property2MID(mid, property):
    MID = list()
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery(
        """PREFIX ns: <http://rdf.freebase.com/ns/> SELECT distinct ?o WHERE {ns:%s ns:%s ?o.}""" % (mid, property))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        for binding in results['results']['bindings']:
            MID.append(binding['o']['value'][27:])
    except:
        pass
    return MID


def SQL_MID2type(mid):
    type = list()
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery(
        """PREFIX ns:<http://rdf.freebase.com/ns/>\nSELECT ?t WHERE {ns:%s ns:type.object.type ?t.}""" % (
            mid))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        for binding in results['results']['bindings']:
            type.append(binding['t']['value'][27:])
    except:
        pass
    return type


def generate(texts, poses, tags, deps, lemmas, if_people, property, target_answer_MID):
    if if_people:
        start_token = 'who'
    else:
        if re.search('\d+-\d+-\d+', target_answer_MID):
            start_token = 'when'
        else:
            start_token = 'what'
    property_str = ' '.join(property.split('_'))
    this_doc = nlp(property_str)
    pos = [token.pos_ for token in this_doc]
    WH_index = tags.index('WP')
    WH_word = lemmas[WH_index]
    new_question = []
    if WH_index != len(tags) - 1:
        if deps[WH_index + 1] == 'aux':
            if lemmas[deps.index('aux')] in ['do']:
                aux_index = deps.index('aux')
                if poses[-1] == 'PUNCT':
                    substitute_part = texts[aux_index + 1:-1]
                else:
                    substitute_part = texts[aux_index + 1:]
                if pos[-1] == 'ADP':
                    new_question.extend(substitute_part)
                    new_question.append('is')
                    new_question.extend(property.split('_'))
                    new_question.append(start_token)
                else:
                    new_question.extend([start_token, 'is', 'the'])
                    new_question.extend(property.split('_'))
                    new_question.append('of')
                    new_question.extend(substitute_part)
            else:
                aux_index = deps.index('aux')
                if poses[-1] == 'PUNCT':
                    substitute_part = texts[aux_index:-1]
                else:
                    substitute_part = texts[aux_index:]
                if WH_word in ['who', 'whose']:
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'person'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'person'])
                        new_question.extend(substitute_part)
                elif WH_word == 'when':
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'time'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'time'])
                        new_question.extend(substitute_part)
                elif WH_word == 'where':
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'place'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'place'])
                        new_question.extend(substitute_part)
                else:
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'thing'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'thing'])
                        new_question.extend(substitute_part)
        elif 'aux' in deps and 'VERB' not in poses[:deps.index('aux')]:
            if lemmas[deps.index('aux')] in ['do']:
                aux_index = deps.index('aux')
                the_thing = texts[1:aux_index]
                if poses[-1] == 'PUNCT':
                    substitute_part = texts[aux_index + 1:-1]
                else:
                    substitute_part = texts[aux_index + 1:]
                if pos[-1] == 'ADP':
                    new_question.append('the')
                    new_question.extend(the_thing)
                    new_question.extend(substitute_part)
                    new_question.append('is')
                    new_question.extend(property.split('_'))
                    new_question.append(start_token)
                else:
                    new_question.extend([start_token, 'is', 'the'])
                    new_question.extend(property.split('_'))
                    new_question.append('of')
                    new_question.append('the')
                    new_question.extend(the_thing)
                    new_question.extend(substitute_part)
            else:
                aux_index = deps.index('aux')
                if poses[-1] == 'PUNCT':
                    substitute_part = texts[aux_index:-1]
                else:
                    substitute_part = texts[aux_index:]
                the_thing = texts[1:aux_index]
                if pos[-1] == 'ADP':
                    new_question.append('the')
                    new_question.extend(the_thing)
                    new_question.extend(substitute_part)
                    new_question.append('is')
                    new_question.extend(property.split('_'))
                    new_question.append(start_token)
                else:
                    new_question.extend([start_token, 'is', 'the'])
                    new_question.extend(property.split('_'))
                    new_question.append('of')
                    new_question.append('the')
                    new_question.extend(the_thing)
                    new_question.extend(substitute_part)
        elif poses[1] != 'VERB':
            ROOT_index = deps.index('ROOT')
            if ROOT_index > WH_index:
                if poses[-1] == 'PUNCT':
                    substitute_part = texts[ROOT_index:-1]
                else:
                    substitute_part = texts[ROOT_index:]
            else:
                substitute_part = texts[:ROOT_index]
            if lemmas[ROOT_index] == 'be':
                if pos[-1] == 'ADP':
                    new_question.extend(substitute_part[1:])
                    new_question.append(substitute_part[0])
                    new_question.extend(property.split('_'))
                    new_question.append(start_token)
                else:
                    new_question.extend([start_token, 'is', 'the'])
                    new_question.extend(property.split('_'))
                    new_question.append('of')
                    new_question.extend(substitute_part[1:])
            else:
                the_thing = texts[1:ROOT_index]
                if pos[-1] == 'ADP':
                    new_question.append('the')
                    new_question.extend(the_thing)
                    new_question.extend(substitute_part)
                    new_question.append('is')
                    new_question.extend(property.split('_'))
                    new_question.append(start_token)
                else:
                    new_question.extend([start_token, 'is', 'the'])
                    new_question.extend(property.split('_'))
                    new_question.append('of')
                    new_question.append('the')
                    new_question.extend(the_thing)
                    new_question.extend(substitute_part)
        else:
            ROOT_index = deps.index('ROOT')
            if ROOT_index > WH_index:
                if poses[-1] == 'PUNCT':
                    substitute_part = texts[ROOT_index:-1]
                else:
                    substitute_part = texts[ROOT_index:]
            else:
                substitute_part = texts[:ROOT_index]
            if lemmas[ROOT_index] == 'be':
                if pos[-1] == 'ADP':
                    new_question.extend(substitute_part[1:])
                    new_question.append(substitute_part[0])
                    new_question.extend(property.split('_'))
                    new_question.append(start_token)
                else:
                    new_question.extend([start_token, 'is', 'the'])
                    new_question.extend(property.split('_'))
                    new_question.append('of')
                    new_question.extend(substitute_part[1:])
            else:
                if WH_word in ['who', 'whose']:
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'person'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'person'])
                        new_question.extend(substitute_part)
                elif WH_word == 'when':
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'time'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'time'])
                        new_question.extend(substitute_part)
                elif WH_word == 'where':
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'place'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'place'])
                        new_question.extend(substitute_part)
                else:
                    if pos[-1] == 'ADP':
                        new_question.extend(['the', 'thing'])
                        new_question.extend(substitute_part)
                        new_question.append('is')
                        new_question.extend(property.split('_'))
                        new_question.append(start_token)
                    else:
                        new_question.extend([start_token, 'is', 'the'])
                        new_question.extend(property.split('_'))
                        new_question.extend(['of', 'the', 'thing'])
                        new_question.extend(substitute_part)
    else:
        ROOT_index = deps.index('ROOT')
        substitute_part = texts[:ROOT_index+1]
        if WH_word in ['who', 'whose']:
            if pos[-1] == 'ADP':
                new_question.extend(['the', 'person'])
                new_question.extend(substitute_part)
                new_question.append('is')
                new_question.extend(property.split('_'))
                new_question.append(start_token)
            else:
                new_question.extend([start_token, 'is', 'the'])
                new_question.extend(property.split('_'))
                new_question.extend(['of', 'the', 'person'])
                new_question.extend(substitute_part)
        elif WH_word == 'when':
            if pos[-1] == 'ADP':
                new_question.extend(['the', 'time'])
                new_question.extend(substitute_part)
                new_question.append('is')
                new_question.extend(property.split('_'))
                new_question.append(start_token)
            else:
                new_question.extend([start_token, 'is', 'the'])
                new_question.extend(property.split('_'))
                new_question.extend(['of', 'the', 'time'])
                new_question.extend(substitute_part)
        elif WH_word == 'where':
            if pos[-1] == 'ADP':
                new_question.extend(['the', 'place'])
                new_question.extend(substitute_part)
                new_question.append('is')
                new_question.extend(property.split('_'))
                new_question.append(start_token)
            else:
                new_question.extend([start_token, 'is', 'the'])
                new_question.extend(property.split('_'))
                new_question.extend(['of', 'the', 'place'])
                new_question.extend(substitute_part)
        else:
            if pos[-1] == 'ADP':
                new_question.extend(['the', 'thing'])
                new_question.extend(substitute_part)
                new_question.append('is')
                new_question.extend(property.split('_'))
                new_question.append(start_token)
            else:
                new_question.extend([start_token, 'is', 'the'])
                new_question.extend(property.split('_'))
                new_question.extend(['of', 'the', 'thing'])
                new_question.extend(substitute_part)
    return new_question


def this_main(npy_file_path, out_file_path):
    output = np.load(npy_file_path, allow_pickle=True)
    output = output.tolist()
    all_info = []
    for i in tqdm(output):
        question = i[0]
        source_output = i[1]
        source_output_MID = i[2]
        question_MID = i[3]
        index = i[4]
        dataset_name = i[5]
        label = i[6]

        doc = nlp(question)
        texts = [token.text for token in doc]
        poses = [token.pos_ for token in doc]
        tags = [token.tag_ for token in doc]
        deps = [token.dep_ for token in doc]
        lemmas = [token.lemma_ for token in doc]
        if 'WP' not in tags:
            continue
        all_new_question = []
        all_target_answer_MIDs = []
        properties = SQL_MID2property(source_output_MID)
        for this_property in properties:
            try:
                target_answer_MIDs = SQL_property2MID(source_output_MID, this_property)
                if target_answer_MIDs == ['']:
                    continue
                types = SQL_MID2type(target_answer_MIDs[0])
                if_people = False
                for this_type in types:
                    if 'people' in this_type:
                        if_people = True
                this_property_tail = list(this_property.split('.'))[-1]
                new_question = generate(texts, poses, tags, deps, lemmas, if_people, this_property_tail, target_answer_MIDs[0])
                if new_question:
                    all_new_question.append(new_question)
                    all_target_answer_MIDs.append(target_answer_MIDs)
            except:
                continue
        if not all_new_question:
            continue
        all_random = [a for a in range(len(all_new_question))]
        random.shuffle(all_random)
        real_all_new_question = [all_new_question[all_random[0]]]
        real_all_target_answer_MIDs = [all_target_answer_MIDs[all_random[0]]]
        for this_index in range(len(real_all_new_question)):
            str_out = TreebankWordDetokenizer().detokenize(real_all_new_question[this_index])
            all_info.append({'primary_question': question,
                             'GT': label,
                             'primary_answer': source_output,
                             'answer_MID': source_output_MID,
                             'target_answer_MID': real_all_target_answer_MIDs[this_index],
                             'new_question': str_out,
                             'question_MID': question_MID,
                             'index': index,
                             'dataset': dataset_name
                             })
    np.save(out_file_path, all_info)



def main():
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--npy_file_path",
        default='npy/webqsp.npy',
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--out_file_path",
        default='PLUS/webqsp_info.npy',
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()
    this_main(args.npy_file_path, args.out_file_path)


if __name__ == "__main__":
    main()