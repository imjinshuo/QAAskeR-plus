## Detailed Test Results and Manual Inspection Record

We provide the raw test result files given by QAAskeR and the manual inspection records.

*All the data are stored in `results` directory.*

---

### Content Structure

```
results
├─1-test_result_of_original_model
│  ├─ComplexKBQA
│  │  ├─ComplexQ_MR1
│  │  │    followup_input.tsv: follow-up inputs of the eligible test cases for original UnifiedQA model with MR1 on SQuAD2 test set.
│  │  │    pass.json: detail information of the passed cases.
│  │  │    violation.json: detail information of the violated cases.
│  │  ├─ComplexQ_MR1+: (content structure is similar to above.)
│  │  ├─WebQSP_MR1: (content structure is similar to above.)
│  │  └─WebQSP_MR1+: (content structure is similar to above.)
│  ├─MACAW
│  │  ├─BoolQ_MR3: (content structure is similar to above.)
│  │  ├─NatQA_MR1: (content structure is similar to above.)
│  │  ├─NatQA_MR1+: (content structure is similar to above.)
│  │  ├─NatQA_MR2: (content structure is similar to above.)
│  │  ├─NatQA_MR2+: (content structure is similar to above.)
│  │  ├─NatQA_MR3: (content structure is similar to above.)
│  │  ├─SQuAD2_MR1: (content structure is similar to above.)
│  │  ├─SQuAD2_MR1+: (content structure is similar to above.)
│  │  ├─SQuAD2_MR2: (content structure is similar to above.)
│  │  ├─SQuAD2_MR2+: (content structure is similar to above.)
│  │  └─SQuAD2_MR3: (content structure is similar to above.)
│  ├─NSM+h
│  │  ├─ComplexQ_MR1: (content structure is similar to above.)
│  │  ├─ComplexQ_MR1+: (content structure is similar to above.)
│  │  ├─WebQSP_MR1: (content structure is similar to above.)
│  │  └─WebQSP_MR1+: (content structure is similar to above.)
│  └─UnifiedQA
│      ├─BoolQ_MR3: (content structure is similar to above.)
│      ├─NatQA_MR1: (content structure is similar to above.)
│      ├─NatQA_MR1+: (content structure is similar to above.)
│      ├─NatQA_MR2: (content structure is similar to above.)
│      ├─NatQA_MR2+: (content structure is similar to above.)
│      ├─NatQA_MR3: (content structure is similar to above.)
│      ├─SQuAD2_MR1: (content structure is similar to above.)
│      ├─SQuAD2_MR1+: (content structure is similar to above.)
│      ├─SQuAD2_MR2: (content structure is similar to above.)
│      ├─SQuAD2_MR2+: (content structure is similar to above.)
│      └─SQuAD2_MR3: (content structure is similar to above.)
├─2-human_inspectation_result
│  ├─MR_BT
│  │  ├─NSM
│  │  │     CWQ.csv: the manual inspectation result on the revealed violations with MR_BT on CWQ test set.
│  │  │     WebQSP.csv: the manual inspectation result on the revealed violations with MR_BT on WebQSP test set.
│  │  └─UnifiedQA
│  │        BoolQ.csv: the manual inspectation result on the revealed violations with MR_BT on BoolQ test set.
│  │        NatQA.csv: the manual inspectation result on the revealed violations with MR_BT on NatQA test set.
│  │        SquAD2.csv: the manual inspectation result on the revealed violations with MR_BT on SquAD2 test set.
│  ├─MR_SR
│  │  ├─NSM
│  │  │     CWQ.csv: the manual inspectation result on the revealed violations with MR_BT on CWQ test set.
│  │  │     WebQSP.csv: the manual inspectation result on the revealed violations with MR_BT on WebQSP test set.
│  │  └─UnifiedQA
│  │        BoolQ.csv: the manual inspectation result on the revealed violations with MR_BT on BoolQ test set.
│  │        NatQA.csv: the manual inspectation result on the revealed violations with MR_BT on NatQA test set.
│  │        SquAD2.csv: the manual inspectation result on the revealed violations with MR_BT on SquAD2 test set.
│  └─QAAskeR+
│         SQuAD2_MR1.csv: the manual inspectation result on the revealed violations with MR1 on SQuAD2 test set.
│         ...(15 files in total)...
│         NatQA_MR3.csv: the manual inspectation result on the revealed violations with MR3 on NatQA test set.
├─3-test_result_of_new_retrained_model_and_fine_tuned_model
│  ├─new_fine_tuned_model
│  │  ├─NSM
│  │  │  ├─ComplexQ_MR1
│  │  │  │     followup_input.tsv: follow-up inputs of the eligible test cases for original UnifiedQA model with MR1 on SQuAD2 test set.
│  │  │  │     pass.json: detail information of the passed cases.
│  │  │  │     violation.json: detail information of the violated cases.
│  │  │  ├─ComplexQ_MR1+: (content structure is similar to above.)
│  │  │  ├─WebQSP_MR1: (content structure is similar to above.)
│  │  │  └─WebQSP_MR1+: (content structure is similar to above.)
│  │  └─UnifiedQA
│  │      ├─BoolQ_MR3: (content structure is similar to above.)
│  │      ├─NatQA_MR1: (content structure is similar to above.)
│  │      ├─NatQA_MR1+: (content structure is similar to above.)
│  │      ├─NatQA_MR2: (content structure is similar to above.)
│  │      ├─NatQA_MR2+: (content structure is similar to above.)
│  │      ├─NatQA_MR3: (content structure is similar to above.)
│  │      ├─SQuAD2_MR1: (content structure is similar to above.)
│  │      ├─SQuAD2_MR1+: (content structure is similar to above.)
│  │      ├─SQuAD2_MR2: (content structure is similar to above.)
│  │      ├─SQuAD2_MR2+: (content structure is similar to above.)
│  │      └─SQuAD2_MR3: (content structure is similar to above.)
│  └─new_retrained_model
│      ├─NSM
│      │  ├─ComplexQ_MR1: (content structure is similar to above.)
│      │  ├─ComplexQ_MR1+: (content structure is similar to above.)
│      │  ├─WebQSP_MR1: (content structure is similar to above.)
│      │  └─WebQSP_MR1+: (content structure is similar to above.)
│      └─UnifiedQA
│          ├─BoolQ_MR3: (content structure is similar to above.)
│          ├─NatQA_MR1: (content structure is similar to above.)
│          ├─NatQA_MR1+: (content structure is similar to above.)
│          ├─NatQA_MR2: (content structure is similar to above.)
│          ├─NatQA_MR2+: (content structure is similar to above.)
│          ├─NatQA_MR3: (content structure is similar to above.)
│          ├─SQuAD2_MR1: (content structure is similar to above.)
│          ├─SQuAD2_MR1+: (content structure is similar to above.)
│          ├─SQuAD2_MR2: (content structure is similar to above.)
│          ├─SQuAD2_MR2+: (content structure is similar to above.)
│          └─SQuAD2_MR3: (content structure is similar to above.)
└─4-test_result_of_google_search
                GoogleSearch-MR1.csv: the test result of MR1 on Google Search service with 20 samples from MKQA dataset.
                GoogleSearch-MR1+.csv: the test result of MR1+ on Google Search service with 20 samples from MKQA dataset.
```

---

*Return to [README](README.md)*
