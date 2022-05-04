import os
import pathlib
import pickle
from os.path import join

import pandas as pd


class Store:
    def __init__(self, root_dir):
        self._root_dir = root_dir
        if not self._root_dir.startswith("s3://"):
            os.makedirs(self._root_dir, exist_ok=True)


class CSVStore(Store):
    def __init__(self, root_dir):
        super(FeatherStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_csv(join(self._root_dir, key) + ".csv")

    def __setitem__(self, key: str, value: pd.DataFrame):
        value.to_feather(join(self._root_dir, key) + ".feather")


class TSVStore(Store):
    def __init__(self, root_dir):
        super(FeatherStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_csv(join(self._root_dir, key) + ".tsv", sep="\t")

    def __setitem__(self, key: str, value: pd.DataFrame):
        value.to_feather(join(self._root_dir, key) + ".feather")


class FeatherStore(Store):
    def __init__(self, root_dir):
        super(FeatherStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_feather(join(self._root_dir, key) + ".feather")

    def __setitem__(self, key: str, value: pd.DataFrame):
        value.to_feather(join(self._root_dir, key) + ".feather")


class PickleStore(Store):
    def __init__(self, root_dir):
        super(PickleStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_pickle(join(self._root_dir, key) + ".pkl")

    def __setitem__(self, key: str, value):
        with open(join(self._root_dir, key) + ".pkl", "wb") as f:
            pickle.dump(value, f)


class UniversalStore(CSVStore, FeatherStore, PickleStore):
    def __init__(self, root_dir):
        FeatherStore.__init__(self, root_dir)
        self._supported_exts = {
            ".csv": CSVStore,
            ".feather": FeatherStore,
            ".pkl": PickleStore,
            ".tsv": TSVStore,
        }

    def __getitem__(self, key: str):
        fmt = self._get_format(key)
        if len(fmt) == 0:
            path = join(self._root_dir, key)
            paths = self._get_possible_paths(path)
            if len(paths) == 0:
                raise Exception(f"{path} does not exist.")
            if len(paths) > 1:
                raise Exception(f"There are two files with the same base name {paths}.")
            path = paths[0]
            return self._supported_exts[fmt].__getitem__(self, key)
        elif fmt not in self._supported_exts:
            raise Exception(f"Format {fmt} is not recognized")
        else:
            return self._supported_exts[fmt].__getitem__(self, key[: -len(fmt)])

    def _get_possible_paths(self, path):
        return [
            path + ext
            for ext in self._supported_exts
            if pathlib.Path(path + ext).exists()
        ]

    def __setitem__(self, key: str, value):
        fmt = self._get_format(key)
        if fmt not in self._supported_exts:
            raise Exception(f"Format {fmt} is not recognized")
        self._supported_exts[fmt].__setitem__(self, key.replace(fmt, ""), value)

    def _get_format(self, path):
        return pathlib.Path(path).suffix
