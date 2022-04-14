import numpy as np
import argparse
import json
import re
from SPARQLWrapper import SPARQLWrapper, JSON


SPARQLPATH = "http://localhost:8890/sparql"
def SQL_entity2name(e):
    if not re.search('^[mg]\.', e): return e
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery("""PREFIX ns:<http://rdf.freebase.com/ns/>\nSELECT ?t WHERE {ns:%s ns:type.object.name ?t.}
    """ %(e))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        name = results['results']['bindings'][0]['t']['value'] if results['results']['bindings'] else '[UNK]'
    except:
        name = '[unk]'
    return name


def m2n(e):
    name = SQL_entity2name(e)
    return name.lower()


def load_dict(filename):
    id2word = dict()
    with open(filename, encoding='utf-8') as f_in:
        for line in f_in:
            word = line.strip()
            id2word[len(id2word)] = word
    return id2word


def main():
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--data_cwq_test_question_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--data_cwq_test_answer_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--data_cwq_topic_entity_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--cwq_output_MID_tsv_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--cwq_npy",
        default=None,
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()
    
    output_MID = []
    with open(args.cwq_output_MID_tsv_file, "r", encoding='utf-8', errors='ignore') as f:
        for line in f:
            this_output_MID = [line.split("\t")]
            this_strip_output_MID = [MID.strip() for MID in this_output_MID]
            output_MID.append(this_strip_output_MID)

    output = []
    from tqdm import tqdm
    for mid_list in tqdm(output_MID):
        this_output= []
        for mid in mid_list:
            name = m2n(mid)
            this_output.append(name)
        output.append(this_output)

    all_question = []
    all_answer = []
    all_MID = []
    all_index = []
    f = open(args.data_cwq_test_question_file, 'r')
    index = -1
    for line in f.readlines():
        index += 1
        all_question.append(line.strip())
        all_index.append(index)

    f = open(args.data_cwq_test_answer_file, 'r')
    for line in f.readlines():
        all_answer.append(list(line.split("\t")))

    f = open(args.data_cwq_topic_entity_file, 'r')
    for line in f.readlines():
        this_line = json.loads(line)
        all_MID.append(list(this_line.keys()))

    data_save_in_npy = []
    for index in range(len(output)):
        for this_output_index in range(len(output[index])):
            if output[index][this_output_index] != '[unk]':
                data_save_in_npy.append(
                    [all_question[index], output[index][this_output_index], output_MID[index][this_output_index], all_MID[index], all_index[index], "cwq", all_answer[index]])
    np.save(args.cwq_npy, data_save_in_npy)


if __name__ == "__main__":
    main()
