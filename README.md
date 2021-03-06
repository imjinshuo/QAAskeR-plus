# Artifact for the Paper "QAAskeR+: A Novel Testing Method for Question Answering Software via Asking Recursive Questions"

This is the artifact for the paper "***QAAskeR+: A Novel Testing Method for Question Answering Software via Asking Recursive Questions***". This artifact supplies the replication package and the supplementary material of the paper. 

This paper is the extended verion of the ASE 2021 Research Track paper ["*Testing Your Question Answering Software via Asking Recursively*"](https://doi.org/10.1109/ASE51524.2021.9678670). The artifact of the conference paper are available [here](https://github.com/imcsq/ASE21-QAAskeR).

Question Answering (QA) software is widely used in daily human life. But at the most time, the users directly trust the returned answers as it's not easy to detect the problem in the returned answers without knowing the corresponding correct answers. 
In this paper, we propose a method named QAAskeR+ based on Metamorphic Testing. QAAskeR+ aims to facilitate the extensible and just-in-time test for the QA systems on the test cases *without the annotated answers*, and is found to be promisingly effective to reveal a few answering issues on 4 state-of-the-art QA models, and the Google Search service.

**This artifact contains:**

1. **Implementation and Usage Instruction of QAAskeR+**, i.e., the python scripts and the concrete instructions to generate the follow-up test cases and measure violation with the three novel MRs. (*please refer to **[`1-tool.md`](1-tool.md)** for details*)

2. **Experiment Replication Package**, i.e., the instruction, codes, and data source for replicating the evaluation reported in the paper. (*please refer to **[`2-replication.md`](2-replication.md)** for details*)

3. **Details of the Heuristic Rules for Declaration Synthesis**, i.e., specific introduction about the heuristic rules involved during synthesizing declaration sentences. (*please refer to **[`3-rules.md`](3-rules.md)** for details*)

4. **Detailed Test Results and Manual Inspection Records** in our evaluation experiment. (*please refer to **[`4-results.md`](4-results.md)** for details*)

*And please refer to **[`INSTALL.md`](INSTALL.md)** for installation instructions.*
