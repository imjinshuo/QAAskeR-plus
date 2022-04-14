import re
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import argparse
from tqdm import tqdm
from transformers import BertTokenizer, BertForTokenClassification
tokenizer = BertTokenizer.from_pretrained('bert-large-cased')



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


def list_to_str(a_list):
    if_start = True
    str_out = ""
    for i in a_list:
        if if_start:
            str_out = str_out + i
            if_start = False
        else:
            str_out = str_out + " " + i
    return str_out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file_path",
        default='Q2S/webqsp.npy',
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--information_file_path",
        default='Q2S2W/webqsp_info.npy',
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--answers_file_path",
        default='Q2S2W/webqsp_ans.npy',
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--for_unilm_file_path",
        default='Q2S2W/webqsp_unilm.npy',
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()

    source_statements = np.load(args.input_file_path, allow_pickle=True)
    source_statements = source_statements.tolist()

    statements = []
    for i in source_statements:
        statement = i["statement"]
        answer = i["answer"]
        answer_MID = i["answer_MID"]
        question_MID = i["question_MID"]
        question = i["question"]
        GT = i["GT"]
        index = i["index"]
        this_dataset = i["dataset"]
        statements.append([statement, answer, answer_MID, question_MID, question, GT, index, this_dataset])


    print_out_data = []
    print_out_data_jiancha = []
    print_out_data_jilu = []
    for a_num in tqdm(range(len(statements))):
        one = statements[a_num]
        final_out = []
        for this_MID in one[3]:
            fina_article = one[0]
            fina_article = str(fina_article).lower()
            this_MID_name = m2n(this_MID)
            if this_MID_name == '[unk]':
                continue
            if this_MID_name not in fina_article:
                continue
            final_answer = this_MID_name
            tokens_article = tokenizer.tokenize(fina_article)
            tokens_answer = tokenizer.tokenize(final_answer)

            final_out.append([one[0], final_answer, this_MID])

            print_out_data.append(list_to_str(tokens_article) + " [SEP] " + list_to_str(tokens_answer))
        print_out_data_jiancha.append(final_out)
        print_out_data_jilu.append({'source_answer': one[1],
                                    'source_question': one[4],
                                    'answer_MID': one[2],
                                    'question_MID': one[3],
                                    'GT': one[5],
                                    'index': one[6],
                                    'dataset': one[7]})

    data = open(args.for_unilm_file_path, 'w', encoding='utf-8')
    for i in print_out_data:
        print(i, file=data)
    data.close()

    np.save(args.information_file_path, print_out_data_jilu)
    np.save(args.answers_file_path, print_out_data_jiancha)


if __name__ == "__main__":
    main()
