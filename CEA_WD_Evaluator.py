'''
Code adapted from https://github.com/city-knowledge-graphs/phd-course/blob/main/python/lab-session3/sem-tab-evaluator/CEA_Evaluator.py
    by @ejimenez-ruiz

Created in 2024
@author: dylanlty
'''

import pandas as pd
import os

class CEA_Evaluator:
    def __init__(self):
        pass

    def _evaluate(self, system_file, gt_file):
        gt_cell_ent = dict()
        gt = pd.read_csv(gt_file, delimiter=',', names=['tab_id', 'row_id', 'col_id', 'entity'],
                         dtype={'tab_id': str, 'col_id': str, 'row_id': str, 'entity': str}, keep_default_na=False)
        for index, row in gt.iterrows():
            cell = '%s %s %s' % (row['tab_id'], row['col_id'], row['row_id'])
            gt_cell_ent[cell] = row['entity']

        correct_cells, annotated_cells = set(), set()
        sub = pd.read_csv(system_file, delimiter=',', names=['tab_id', 'row_id', 'col_id', 'entity'],
                          dtype={'tab_id': str, 'col_id': str, 'row_id': str, 'entity': str}, keep_default_na=False)

        for index, row in sub.iterrows():
            cell = '%s %s %s' % (row['tab_id'], row['col_id'], row['row_id'])
            if cell in gt_cell_ent:
                if cell in annotated_cells:
                    raise Exception("Duplicate cells in the submission file")
                else:
                    annotated_cells.add(cell)

                annotation = row['entity']
                #if not annotation.lower() == 'nil' and not annotation.startswith('http://dbpedia.org/resource/'):
                #    annotation = 'http://dbpedia.org/resource/' + annotation

                if annotation.lower() in gt_cell_ent[cell].lower().split():
                    correct_cells.add(cell)
                
                ## To print cell incorrectly annotated
                #else:
                #    print('%s,%s' % (cell.replace(' ', ','), gt_cell_ent[cell]))

        precision = len(correct_cells) / len(annotated_cells) if len(annotated_cells) > 0 else 0.0
        recall = len(correct_cells) / len(gt_cell_ent.keys())
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        main_score = f1
        secondary_score = precision
        print('%.3f %.3f %.3f' % (f1, precision, recall))

        _result_object = {
            "score/f1": main_score,
            "score_secondary/precision": secondary_score
        }
        return _result_object


if __name__ == "__main__":
    # Lets assume the the ground_truth is a CSV file
    # and is present at data/ground_truth.csv
    # and a sample submission is present at data/sample_submission.csv

    gt_file = "data/gt/cea_gt.csv"

    system_files = [
        "output/cea-gemini-1.5-flash.csv",
        "output/cea-llama3-8b-instruct.csv",
        "output/cea-gpt-4o-mini.csv"
    ]

    # Instantiate an evaluator
    evaluator = CEA_Evaluator()
    # Evaluate
    print("\n--------------------")
    for system_file in system_files:
        print(f"{system_file}\n")
        print("f1 precision recall")
        result = evaluator._evaluate(system_file, gt_file)
        print(f"\n{result}\n--------------------")
    print()


    
