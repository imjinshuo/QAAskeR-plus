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
        "--data_webqsp_test_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--data_webqsp_entity_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--webqsp_output_MID_tsv_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--webqsp_npy",
        default=None,
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()

    output_MID = []
    with open(args.webqsp_output_MID_tsv_file, "r", encoding='utf-8', errors='ignore') as f:
        for line in f:
            this_output_MID = [line.split("\t")]
            this_strip_output_MID = [MID.strip() for MID in this_output_MID]
            output_MID.append(this_strip_output_MID)

    output = []
    from tqdm import tqdm
    for mid_list in tqdm(output_MID):
        this_output = []
        for mid in mid_list:
            name = m2n(mid)
            this_output.append(name)
        output.append(this_output)

    id2MID = load_dict(args.data_webqsp_entity_file)
    all_question = []
    all_answer = []
    all_MID = []
    all_index = []
    with open(args.data_webqsp_test_file) as f_in:
        lines = f_in.readlines()
        for line in lines:
            data = json.loads(line)
            all_question.append(data['question'])
            all_answer.append(data['answers'])
            MIDs =[id2MID[i] for i in data['entities']]
            all_MID.append(MIDs)
            all_index.append(data['id'])


    data_save_in_npy = []
    for index in range(len(output)):
        for this_output_index in range(len(output[index])):
            if output[index][this_output_index] != '[unk]':
                data_save_in_npy.append(
                    [all_question[index], output[index][this_output_index], output_MID[index][this_output_index],
                     all_MID[index], all_index[index], "webqsp", all_answer[index]])
    np.save(args.webqsp_npy, data_save_in_npy)


if __name__ == "__main__":
    main()
