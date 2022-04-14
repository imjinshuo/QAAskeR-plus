import argparse
import numpy as np
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_to_information",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--path_to_output_from_model",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--path_to_invalid_index",
        default=None,
        type=str,
        required=False,
        help=""
    )
    parser.add_argument(
        "--path_to_violation",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--path_to_pass",
        default=None,
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()
    all_info = np.load(args.path_to_information, allow_pickle=True)
    all_info = all_info.tolist()

    follow_output = []
    with open(args.path_to_output_from_model, "r", encoding='utf-8', errors='ignore') as f:
        for line in f:
            this_output_MID = [line.split("\t")]
            this_strip_output_MID = [MID.strip() for MID in this_output_MID]
            follow_output.append(this_strip_output_MID)

    all_invalid_index = []
    if path_to_invalid_index is not None:
        all_invalid_index = np.load(args.path_to_invalid_index, allow_pickle=True)
        all_invalid_index = all_invalid_index.tolist()
    target_answer = [sample['target_answer_MID'] for sample in all_info]
    violations = []
    pass_samples = []

    for index in range(len(target_answer)):
        if index in all_invalid_index:
            continue
        this_target_answer = target_answer[index]
        this_follow_output = follow_output[index]
        if this_target_answer in this_follow_output:
            pass_samples.append(index)
        else:
            violations.append(index)

    data_violation = open(args.path_to_violation, 'w', encoding='utf-8')
    data_pass = open(args.path_to_pass, 'w', encoding='utf-8')

    from tqdm import tqdm
    for i in tqdm(violations):
        this_new_answer = follow_output[i]
        this_new_answer_name = []
        for mid in this_new_answer:
            name = m2n(mid)
            this_new_answer_name.append(name)

        this_question_MID = all_info[i]['question_MID']
        this_new_question_MID = []
        for mid in this_question_MID:
            name = m2n(mid)
            this_new_question_MID.append(name)
        print("{\"source_question\": \"" + str(all_info[i]['primary_question'])
              + "\", \"source_question_entity_MID\": \"" + str(this_new_question_MID)
              + "\", \"ground_truth\": \"" + str(all_info[i]['GT'])
              + "\", \"source_answer\": \"" + str(all_info[i]['primary_answer'])
              + "\", \"source_answer_MID\": \"" + str(all_info[i]['answer_MID'])
              + "\", \"declarative_sentence\": \"" + str(all_info[i]['statement'])
              + "\", \"target_answer\": \"" + str(all_info[i]['target_answer'])
              + "\", \"target_answer_MID\": \"" + str(all_info[i]['target_answer_MID'])
              + "\", \"new_question\": \"" + str(all_info[i]['new_question'])
              + "\", \"new_answer\": \"" + str(this_new_answer_name)
              + "\", \"rouge_1_p\": \"" + str(all_info[i]['rouge_1_p'])
              + "\", \"rouge_1_r\": \"" + str(all_info[i]['rouge_1_r'])
              + "\", \"index\": \"" + str(all_info[i]['index'])
              + "\", \"dataset\": \"" + str(all_info[i]['dataset']) + "\"}",
              file=data_violation)

    for i in pass_samples:
        print("{\"source_question\": \"" + str(all_info[i]['primary_question'])
              + "\", \"source_question_entity_MID\": \"" + str(all_info[i]['question_MID'])
              + "\", \"ground_truth\": \"" + str(all_info[i]['GT'])
              + "\", \"source_answer\": \"" + str(all_info[i]['primary_answer'])
              + "\", \"source_answer_MID\": \"" + str(all_info[i]['answer_MID'])
              + "\", \"declarative_sentence\": \"" + str(all_info[i]['statement'])
              + "\", \"target_answer\": \"" + str(all_info[i]['target_answer'])
              + "\", \"target_answer_MID\": \"" + str(all_info[i]['target_answer_MID'])
              + "\", \"new_question\": \"" + str(all_info[i]['new_question'])
              + "\", \"new_answer\": \"" + str(follow_output[i])
              + "\", \"rouge_1_p\": \"" + str(all_info[i]['rouge_1_p'])
              + "\", \"rouge_1_r\": \"" + str(all_info[i]['rouge_1_r'])
              + "\", \"index\": \"" + str(all_info[i]['index'])
              + "\", \"dataset\": \"" + str(all_info[i]['dataset']) + "\"}",
              file=data_pass)
    print("violations number: ", len(violations))
    print("pass number: ", len(pass_samples))

    data_violation.close()
    data_pass.close()


if __name__ == "__main__":
    main()
