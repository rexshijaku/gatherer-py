import pandas as pd
import os
import glob


class FHandler:
    __encoding = None

    def __init__(self, encoding):
        self.__encoding = encoding

    def mergeFiles(self, all_files_path, headers=None):
        merge_these_for_dataset = glob.glob(os.path.join(all_files_path, "*.csv"))

        if len(merge_these_for_dataset) < 1:
            print("no file to merge")
            return []

        combined_csv = pd.concat(
            [pd.read_csv(f, header=headers, encoding=self.__encoding) for f in merge_these_for_dataset],
            sort=False)

        return combined_csv

    def save(self, merge_result, save_path):
        merge_result.to_csv(save_path, index=False, header=None, encoding=self.__encoding)
