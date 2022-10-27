import os
import pathlib
import pickle
from os.path import join

import pandas as pd


class Store:
    def __init__(self, root_dir):
        self._root_dir = root_dir
        os.makedirs(self._root_dir, exist_ok=True)

    def __setitem__(self, key: str, value: pd.DataFrame):
        if not isinstance(value, pd.DataFrame):
            raise TypeError(f"value should be pd.DataFrame, but found {type(value)}")


class CsvStore(Store):
    def __init__(self, root_dir):
        super(CsvStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_csv(join(self._root_dir, key) + ".csv")

    def __setitem__(self, key: str, value: pd.DataFrame):
        super().__setitem__(key, value)
        value.to_csv(join(self._root_dir, key) + ".csv", index=False)


class FeatherStore(Store):
    def __init__(self, root_dir):
        super(FeatherStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_feather(join(self._root_dir, key) + ".feather")

    def __setitem__(self, key: str, value: pd.DataFrame):
        super().__setitem__(key, value)
        value.to_feather(join(self._root_dir, key) + ".feather")


class PickleStore(Store):
    def __init__(self, root_dir):
        super(PickleStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_pickle(join(self._root_dir, key) + ".pkl")

    def __setitem__(self, key: str, value):
        with open(join(self._root_dir, key) + ".pkl", "wb") as f:
            pickle.dump(value, f)


class DocBinStore(PickleStore):
    def __init__(self, root_dir):
        super(DocBinStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        doc_bin_bytes = super().__getitem__(key)
        return DocBin().from_bytes(doc_bin_bytes)

    def __setitem__(self, key: str, docs):
        doc_bin = DocBin(store_user_data=False)
        for doc in docs:
            doc_bin.add(doc)
        doc_bin_bytes = doc_bin.to_bytes()
        super().__setitem__(key, doc_bin_bytes)


class JsonStore(Store):
    def __init__(self, root_dir):
        super(JsonStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        with open(join(self._root_dir, key) + ".json", "r") as f:
            return json.load(f)

    def __setitem__(self, key: str, value):
        with open(join(self._root_dir, key) + ".json", "w") as f:
            json.dump(value, f)


class JsonlStore(Store):
    def __init__(self, root_dir):
        super(JsonlStore, self).__init__(root_dir)

    def __getitem__(self, key: str):
        return pd.read_json(join(self._root_dir, key) + ".jsonl", lines=True)

    def __setitem__(self, key: str, value):
        with open(join(self._root_dir, key) + ".jsonl", "w") as f:
            for line in value:
                f.write(json.dumps(line) + "\n")


class UniversalStore(Store):
    def __init__(self, root_dir):
        Store.__init__(self, root_dir)
        self._supported_fmts = {
            ".feather": FeatherStore,
            ".csv": CsvStore,
            ".pkl": PickleStore,
            ".json": JsonStore,
            ".jsonl": JsonlStore,
        }

    def __getitem__(self, key: str):
        path = join(self._root_dir, key)
        paths = self._get_possible_paths(path)
        if len(paths) == 0:
            raise Exception(f"{path} does not exist.")
        if len(paths) > 1:
            raise Exception(f"There are two files with the same base name {paths}.")
        fmt = self._get_format(paths[0])
        if fmt not in self._supported_fmts:
            raise Exception(f"Format {fmt} is not recognized")
        key = self.__path_with_no_fmt(key, fmt)
        return self._supported_fmts[fmt].__getitem__(self, key)

    def __setitem__(self, key: str, value):
        fmt = self._get_format(key)
        if fmt not in self._supported_fmts:
            raise Exception(f"Format {fmt} is not recognized")
        key = self.__path_with_no_fmt(key, fmt)
        self._supported_fmts[fmt].__setitem__(self, key, value)

    def _get_possible_paths(self, path):
        return [
            self.__path_with_fmt(path, fmt)
            for fmt in self._supported_fmts
            if pathlib.Path(self.__path_with_fmt(path, fmt)).exists()
        ]

    def __path_with_fmt(self, path, fmt):
        if path.endswith(fmt):
            return path
        return path + fmt

    def __path_with_no_fmt(self, path, fmt):
        if path.endswith(fmt):
            return path[: -len(fmt)]
        return path

    def _get_format(self, path):
        return pathlib.Path(path).suffix
