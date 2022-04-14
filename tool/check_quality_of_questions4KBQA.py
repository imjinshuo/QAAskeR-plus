from Q2S import change
import json
import csv
import argparse
import numpy as np
from rouge import Rouge
from tqdm import tqdm

rouge = Rouge()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--new_question_file_path",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--information_file_path",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--answers_file_path",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--out_information_file_path",
        default=None,
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()
    with open(args.new_question_file_path, "r", encoding="utf-8") as f:
        lines_nq = f.readlines()

    new_questions = []
    for line in lines_nq:
        new_questions.append(line.strip("\n"))

    childrens = np.load(args.answers_file_path, allow_pickle=True)
    source_info = np.load(args.information_file_path, allow_pickle=True)
    source_questions = []
    source_answers = []
    answer_MID = []
    question_MID = []
    GT = []
    index = []
    this_dataset = []
    for i in source_info:
        source_questions.append(i["source_question"])
        source_answers.append(i["source_answer"])
        answer_MID.append(i["answer_MID"])
        question_MID.append(i["question_MID"])
        GT.append(i["GT"])
        index.append(i["index"])
        this_dataset.append(i["dataset"])


    pass_num = 0
    not_pass_num = 0
    none_question = 0
    num = 0

    all_info = []
    for children_num in tqdm(range(len(childrens))):
        children = childrens[children_num]
        children_scores = []
        for child in children:
            statement = child[0]
            answer = child[1]
            target_answer_MID = child[2]
            if len(new_questions[num]) == 0:
                none_question += 1
                num += 1
                continue
            new_statement = change(new_questions[num], answer)
            if new_statement != None:
                statement = statement.lower()
                new_statement = new_statement.lower()
                scores = rouge.get_scores(hyps=[new_statement], refs=[statement])
                rouge_1_p = scores[0]['rouge-1']['p']
                rouge_1_r = scores[0]['rouge-1']['r']
                if rouge_1_p > 0.7 and rouge_1_r > 0.7:
                    children_scores.append([rouge_1_p, rouge_1_r, children_num, statement, answer, new_questions[num], target_answer_MID])
            num += 1
        if children_scores == []:
            not_pass_num += 1
            continue
        a = []
        for i in range(len(children_scores)):
            a.append(i)
        np.random.shuffle(a)
        rdm = a[0]
        all_info.append({'primary_question': source_questions[children_scores[rdm][2]],
                         'GT': GT[children_scores[rdm][2]],
                         'primary_answer': source_answers[children_scores[rdm][2]],
                         'statement': children_scores[rdm][3],
                         'target_answer': children_scores[rdm][4],
                         'target_answer_MID': children_scores[rdm][6],
                         'new_question': children_scores[rdm][5],
                         'answer_MID': answer_MID[children_scores[rdm][2]],
                         'question_MID': question_MID[children_scores[rdm][2]],
                         'rouge_1_p': children_scores[rdm][0],
                         'rouge_1_r': children_scores[rdm][1],
                         'index': index[children_scores[rdm][2]],
                         'dataset': this_dataset[children_scores[rdm][2]]})
        pass_num += 1

    print("pass: ", pass_num)
    print("fail: ", not_pass_num)
    np.save(args.out_information_file_path, all_info)


if __name__ == "__main__":
    main()