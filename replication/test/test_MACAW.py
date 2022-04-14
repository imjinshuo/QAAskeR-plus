from macaw.utils import load_model, run_macaw
from tqdm import tqdm
import argparse


def run_model(data, all_question_passage, model_dict):
    all_input = []
    for question_passage in all_question_passage:
        if ' \\n ' in question_passage:
            question, context = question_passage.split(' \\n ')
        else:
            question, context = question_passage.split('\\n')
        input = "Q: " + question + "\nC: " + context + "\nA"
        all_input.append(input)
    for input in tqdm(all_input, desc="Evaluating"):
        out = run_macaw(input, model_dict)
        this_out = out["output_slots_list"][0]['answer']
        print(this_out, file=data)


def main():
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--model_name",
        default='allenai/macaw-large',
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--data_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    parser.add_argument(
        "--output_file",
        default=None,
        type=str,
        required=True,
        help=""
    )
    args = parser.parse_args()
    all_question_passage = []
    with open(args.data_file, "r", encoding='utf-8', errors='ignore') as f:
        for line in f:
            question, answer = line.split("\t")
            all_question_passage.append(question)
    data = open(args.output_file, 'w', encoding='utf-8')
    model_dict = load_model(args.model_name, cuda_devices=[0])
    run_model(data, all_question_passage, model_dict)
    data.close()


if __name__ == "__main__":
    main()