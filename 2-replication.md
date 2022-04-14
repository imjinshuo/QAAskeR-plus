## Experiment Replication Package

We provide the codes to replicate our experiments, including the scripts to train the t5-large-based UnifiedQA model and the scripts to answer the given test cases with the trained UnifiedQA model.

*All the codes for replicating the evaluation are stored in `replication` directory.*

---

### Data source
* For TBQA(UnifedQA and MACAW)

    * We adopt the pre-processed SQuAD2, BoolQ, and NatQA datasets provided by UnifiedQA, which can be accessed at https://console.cloud.google.com/storage/browser/unifiedqa/data.
    * The hybrid training set is the combination of the training set from SQuAD2, BoolQ, and NatQA.

* For KBQA(NSM+h and ComplexKBQA)

  * We adopt the pre-processed WebQSP and CWQ datasets provided by NSM+h and ComplexKBQA, which can be accessed at https://drive.google.com/drive/folders/1qRXeuoL-ArQY7pJFnMpNnBu0G-cOz6xv and https://drive.google.com/drive/folders/1sAOUiFbk2ujfXUityIq51p14j9E4HCZ8, respectively.

---

### Usage Instruction for UnifiedQA

1) run `train/cli.py` to train the UnifiedQA model (SUT) on the hybrid training set with the hyper-parameters declared in our paper.
    ```bash
    python train/cli.py \
    --size large \
    --do_train \
    --output_dir path/to/output/dir/to/save/model/file \
    --train_file path/to/the/hybrid/train/tsv/file \
    --predict_file path/to/dev/tsv/file \
    --train_batch_size 3 \
    --predict_batch_size 8 \
    --do_lowercase \
    --eval_period 5000 \
    --learning_rate 2e-5 \
    --gradient_accumulation_steps 5 \
    --wait_step 10
    ```
2) run `test/test_UnifiedQA.py` to get SUT's outputs on the samples from the test set of each dataset, which are used as the source test cases.
    ```bash
    python test/test_UnifiedQA.py \
    --model_name allenai/unifiedqa-t5-large \
    --model_path path/to/model \
    --data_file path/to/dev/tsv/file \
    --output_file path/to/output/tsv/file
    # model_path is the path to the saved best checkpoint (finetuned model) obtained from step 1).
    ```
3) for each dataset, prepare the source test case information (by aggregating each source input and the corresponding source output into one information item) and dump the information into the corresponding `.npy` file.
    ```bash
    python dataset/SQuAD2.py \
    --data_SQuAD2_dev_tsv path/to/source/input/tsv/file \
    --SQuAD2_output_file path/to/source/output/tsv/file \
    --SQuAD2_npy path/to/output/combined/npy/file
    
    python dataset/NatQA.py \
    --data_NatQA_dev_tsv path/to/source/input/tsv/file \
    --NatQA_output_file path/to/source/output/tsv/file \
    --NatQA_npy path/to/output/combined/npy/file
    
    python dataset/BoolQ.py \
    --data_BoolQ_dev_tsv path/to/source/input/tsv/file \
    --BoolQ_output_file path/to/source/output/tsv/file \
    --BoolQ_npy path/to/output/combined/npy/file
    ```
4) for each dataset, run `QAAskeR` to prepare the follow-up inputs with each MR, which are dumped into some `.tsv` files. *(refer to `1-tool.md` for details)*
5) run `test/test_model.py` to get SUT output for each of the follow-up inputs and dump the follow-up outputs into the corresponding `.tsv` files.
6) run `QAAskeR` to measure the violation and form the test report. *(refer to `1-tool.md` for details)*

---

### Usage Instruction for MACAW

1) run `test/test_MACAW.py` to get MACAW's outputs on the samples from the test set of each dataset, which are used as the source test cases.
    ```bash
    python test/test_MACAW.py \
    --model_name allenai/macaw-large \
    --data_file path/to/dev/tsv/file \
    --output_file path/to/output/tsv/file.
    ```
2) following steps are the same to (3) - (6) steps of UnifiedQA *(refer to `Usage Instruction for UnifiedQA` part for details)*

---

### Usage Instruction for NSM+h

1) follow [NSM+h](https://github.com/RichardHGL/WSDM2021_NSM) to train a NSM+h model.
2) for each dataset, follow [NSM+h](https://github.com/RichardHGL/WSDM2021_NSM) to get the model's output and put it into a `.tsv` file, where each line contains an answer, a list of entities splited by `'\t'`, for a piece of question.
3) for each dataset, prepare the source test case information (by aggregating each source input and the corresponding source output into one information item) and dump the information into the corresponding `.npy` file.
    ```bash
    python dataset/WebQSP4NSM.py \
    --data_webqsp_test_file path/to/source/input/file \
    --data_webqsp_entity_file path/to/enttity/file \
    --webqsp_output_MID_tsv_file path/to/source/output/tsv/file \
    --webqsp_npy path/to/output/combined/npy/file
    # data_webqsp_entity_file is the path to the entity file downloaded from https://drive.google.com/drive/folders/1qRXeuoL-ArQY7pJFnMpNnBu0G-cOz6xv
    
    python dataset/CWQ4NSM.py \
    --data_cwq_test_file path/to/source/input/file \
    --data_cwq_entity_file path/to/enttity/file \
    --cwq_output_MID_tsv_file path/to/source/output/tsv/file \
    --cwq_npy path/to/output/combined/npy/file
    # data_cwq_entity_file is the path to the entity file downloaded from https://drive.google.com/drive/folders/1qRXeuoL-ArQY7pJFnMpNnBu0G-cOz6xv
    ```
4) for each dataset, run `QAAskeR` to prepare the follow-up inputs with each MR, which are dumped into some `.npy` files. *(refer to `1-tool.md` for details)*
5) follow [NSM+h](https://github.com/RichardHGL/WSDM2021_NSM) to preprocess the follow-up inputs.
6) Then, similar to step (2), get model's outputs for the preprocessed follow-up inputs and put them into `.tsv` file.
7) run `QAAskeR` to measure the violation and form the test report. *(refer to `1-tool.md` for details)*

---

### Usage Instruction for ComplexKBQA

1) follow [ComplexKBQA](https://github.com/lanyunshi/Multi-hopComplexKBQA) to train a NSM+h model.
2) for each dataset, follow [ComplexKBQA](https://github.com/lanyunshi/Multi-hopComplexKBQA) to get the model's output and put it into a `.tsv` file, where each line contains an answer, a list of entities splited by `'\t'`, for a piece of question.
3) for each dataset, prepare the source test case information (by aggregating each source input and the corresponding source output into one information item) and dump the information into the corresponding `.npy` file.
    ```bash
    python dataset/WebQSP4ComplexKBQA.py \
    --data_webqsp_test_question_file path/to/source/input/question/file \
    --data_webqsp_test_answer_file path/to/source/input/answer/file \
    --data_webqsp_topic_entity_file path/to/source/input/topic_entity/file \
    --webqsp_output_MID_tsv_file path/to/source/output/tsv/file \
    --webqsp_npy path/to/output/combined/npy/file
    # data_webqsp_topic_entity_file is the path to the topic_entity file downloaded from https://drive.google.com/drive/folders/1sAOUiFbk2ujfXUityIq51p14j9E4HCZ8
    
    python dataset/CWQ4ComplexKBQA.py \
    --data_cwq_test_question_file path/to/source/input/question/file \
    --data_cwq_test_answer_file path/to/source/input/answer/file \
    --data_cwq_topic_entity_file path/to/source/input/topic_entity/file \
    --cwq_output_MID_tsv_file path/to/source/output/tsv/file \
    --cwq_npy path/to/output/combined/npy/file
    # data_webqsp_topic_entity_file is the path to the topic_entity file downloaded from https://drive.google.com/drive/folders/1sAOUiFbk2ujfXUityIq51p14j9E4HCZ8
    ```
4) for each dataset, run `QAAskeR` to prepare the follow-up inputs with each MR, which are dumped into some `.npy` files. *(refer to `1-tool.md` for details)*
5) follow [ComplexKBQA](https://github.com/lanyunshi/Multi-hopComplexKBQA) to preprocess the follow-up inputs.
6) Then, similar to step (2), get model's outputs for the preprocessed follow-up inputs and put them into `.tsv` file.
7) run `QAAskeR` to measure the violation and form the test report. *(refer to `1-tool.md` for details)*

---

*Return to [README](README.md)*
