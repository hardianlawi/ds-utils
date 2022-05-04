import torch
from pytorch_lightning import LightningDataModule, LightningModule
from torch.utils.data import DataLoader, Dataset
from torch.utils.data._utils.collate import default_collate
from torchmetrics import Accuracy, F1Score, Precision, Recall
from transformers import (
    AdamW,
    AutoConfig,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup,
)


def text_pair_classification_batch_collate(batch, tokenize_fn):
    batch = default_collate(batch)
    parents, children, labels = batch
    encodings = tokenize_fn(parents, children)
    encodings["labels"] = labels
    return encodings


class TextPairClassificationDataset(Dataset):
    def __init__(self, df):
        self.parents = df["parent"].values
        self.children = df["child"].values
        self.labels = df["label"].values

    def __getitem__(self, idx):
        return (self.parents[idx], self.children[idx], self.labels[idx])

    def __len__(self):
        return len(self.parents)


class TextPairClassificationLightningDataModule(LightningDataModule):
    def __init__(self, dfs, tokenizer, max_length, batch_size=1, num_workers=1):
        super().__init__()
        self.dfs = dfs
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.batch_size = batch_size
        self.num_workers = num_workers

    def _tokenize(self, parents, children):
        return self.tokenizer(
            parents,
            children,
            max_length=self.max_length,
            padding=True,
            truncation=True,
            return_token_type_ids=True,
            return_tensors="pt",
        )

    def train_dataloader(self):
        return DataLoader(
            TextPairClassificationDataset(self.dfs["train"]),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
            collate_fn=lambda x: text_pair_classification_batch_collate(
                x, self._tokenize
            ),
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            TextPairClassificationDataset(self.dfs["val"]),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
            collate_fn=lambda x: text_pair_classification_batch_collate(
                x, self._tokenize
            ),
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            TextPairClassificationDataset(self.dfs["test"]),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
            collate_fn=lambda x: text_pair_classification_batch_collate(
                x, self._tokenize
            ),
            pin_memory=True,
        )

    def predict_dataloader(self):
        return self.test_dataloader()


class DefaultMetrics:
    def __init__(self, num_classes):
        self.metrics = [
            ("acc", Accuracy(num_classes=num_classes, average="micro")),
            ("f1", F1Score(num_classes=num_classes, average="micro")),
            ("precision", Precision(num_classes=num_classes, average="micro")),
            ("recall", Recall(num_classes=num_classes, average="micro")),
        ]
        if num_classes > 2:
            self.metrics += [
                ("macro_acc", Accuracy(num_classes=num_classes, average="macro")),
                ("macro_f1", F1Score(num_classes=num_classes, average="macro")),
                (
                    "macro_precision",
                    Precision(num_classes=num_classes, average="macro"),
                ),
                ("macro_recall", Recall(num_classes=num_classes, average="macro")),
            ]

    def __iter__(self):
        for name, metric in self.metrics:
            yield name, metric


class TextPairClassificationLightningModule(LightningModule):
    def __init__(
        self,
        model_name_or_path,
        num_classes,
        lr=1e-5,
        weight_decay=0.001,
        epsilon=1e-8,
        num_warmup_steps=0,
        max_norm=10.0,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.model_name_or_path = model_name_or_path

        self.config = AutoConfig.from_pretrained(model_name_or_path)
        self.config.num_labels = num_classes

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name_or_path, config=self.config
        )

        self.metrics = {}
        for mode in ["train", "val", "test"]:
            self.metrics[mode] = DefaultMetrics(num_classes)
            for name, metric in self.metrics[mode]:
                setattr(self, f"{mode}_{name}", metric)

    def setup(self, stage=None) -> None:
        if stage != "fit":
            return

        train_loader = self.trainer.datamodule.train_dataloader()
        ab_size = self.trainer.accumulate_grad_batches
        self.total_steps = len(train_loader) * float(self.trainer.max_epochs) // ab_size

        # Use below if using multiple GPUs
        # tb_size = self.hparams.train_batch_size * max(1, self.trainer.gpus)
        # self.total_steps = (len(train_loader.dataset) // tb_size) // ab_size

    def forward(self, inputs):
        outputs = self.model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            labels=inputs.get("labels"),
            token_type_ids=inputs["token_type_ids"],
            return_dict=False,
        )
        if "labels" not in inputs:
            return outputs[0]
        return outputs

    def training_step(self, batch, batch_idx):
        loss, logits = self(batch)
        preds = logits.argmax(axis=1)
        labels = batch["labels"]
        for name, metric in self.metrics["train"]:
            metric(preds, labels)
            self.log(
                f"train_{name}",
                metric,
                on_step=True,
                on_epoch=True,
                prog_bar=True,
                logger=True,
            )

        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )

        torch.nn.utils.clip_grad_norm_(
            parameters=self.model.parameters(), max_norm=self.hparams.max_norm
        )

        return {"loss": loss}

    def validation_step(self, batch, batch_idx):
        loss, logits = self(batch)
        preds = logits.argmax(axis=1)
        labels = batch["labels"]
        for name, metric in self.metrics["val"]:
            metric(preds, labels)
            self.log(
                f"val_{name}",
                metric,
                on_step=False,
                on_epoch=True,
                prog_bar=True,
                logger=True,
            )

        self.log(
            "val_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True
        )
        return preds

    def test_step(self, batch, batch_idx):
        loss, logits = self(batch)
        preds = logits.argmax(axis=1)
        labels = batch["labels"]
        for name, metric in self.metrics["test"]:
            metric(preds, labels)
            self.log(
                f"test_{name}",
                metric,
                on_step=False,
                on_epoch=True,
                prog_bar=True,
                logger=True,
            )

        self.log(
            "test_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True
        )
        return preds

    def configure_optimizers(self):
        """Prepare optimizer and schedule (linear warmup and decay)"""
        model = self.model
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": self.hparams.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.0,
            },
        ]
        optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=self.hparams.lr,
            eps=self.hparams.epsilon,
        )

        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.hparams.num_warmup_steps,
            num_training_steps=self.total_steps,
        )
        scheduler = {"scheduler": scheduler, "interval": "step", "frequency": 1}
        return [optimizer], [scheduler]


class TextClassificationDataset(Dataset):
    def __init__(self, df):
        self.sentences = df["sentence"].values
        self.labels = df["label"].values

    def __getitem__(self, idx):
        return self.sentences[idx], self.labels[idx]

    def __len__(self):
        return len(self.sentences)


def text_classification_batch_collate(batch, tokenize_fn):
    batch = default_collate(batch)
    sentences, labels = batch
    encodings = tokenize_fn(list(sentences))
    encodings["labels"] = labels
    return encodings


class TextClassificationLightningDataModule(LightningDataModule):
    def __init__(self, dfs, tokenizer, max_length, batch_size=1, num_workers=1):
        super().__init__()
        self.dfs = dfs
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.batch_size = batch_size
        self.num_workers = num_workers

    def _tokenize(self, sentences):
        return self.tokenizer(
            sentences,
            max_length=self.max_length,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

    def train_dataloader(self):
        return DataLoader(
            TextClassificationDataset(self.dfs["train"]),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
            collate_fn=lambda x: text_classification_batch_collate(x, self._tokenize),
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            TextClassificationDataset(self.dfs["val"]),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
            collate_fn=lambda x: text_classification_batch_collate(x, self._tokenize),
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            TextClassificationDataset(self.dfs["test"]),
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=False,
            collate_fn=lambda x: text_classification_batch_collate(x, self._tokenize),
            pin_memory=True,
        )

    def predict_dataloader(self):
        return self.test_dataloader()


class TextClassificationLightningModule(LightningModule):
    def __init__(
        self,
        model_name_or_path,
        num_classes,
        lr=1e-5,
        weight_decay=0.001,
        epsilon=1e-8,
        num_warmup_steps=0,
        max_norm=10.0,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.model_name_or_path = model_name_or_path

        self.config = AutoConfig.from_pretrained(model_name_or_path)
        self.config.num_labels = num_classes

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name_or_path, config=self.config
        )

        self.metrics = {}
        for mode in ["train", "val", "test"]:
            self.metrics[mode] = DefaultMetrics(num_classes)
            for name, metric in self.metrics[mode]:
                setattr(self, f"{mode}_{name}", metric)

    def setup(self, stage=None) -> None:
        if stage != "fit":
            return

        train_loader = self.trainer.datamodule.train_dataloader()
        ab_size = self.trainer.accumulate_grad_batches
        self.total_steps = len(train_loader) * float(self.trainer.max_epochs) // ab_size

        # Use below if using multiple GPUs
        # tb_size = self.hparams.train_batch_size * max(1, self.trainer.gpus)
        # self.total_steps = (len(train_loader.dataset) // tb_size) // ab_size

    def forward(self, inputs):
        outputs = self.model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            labels=inputs.get("labels"),
            return_dict=False,
        )
        if "labels" not in inputs:
            return outputs[0]
        return outputs

    def training_step(self, batch, batch_idx):
        loss, logits = self(batch)
        preds = logits.argmax(axis=1)
        labels = batch["labels"]
        for name, metric in self.metrics["train"]:
            metric(preds, labels)
            self.log(
                f"train_{name}",
                metric,
                on_step=True,
                on_epoch=True,
                prog_bar=True,
                logger=True,
            )

        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )

        torch.nn.utils.clip_grad_norm_(
            parameters=self.model.parameters(), max_norm=self.hparams.max_norm
        )

        return {"loss": loss}

    def validation_step(self, batch, batch_idx):
        loss, logits = self(batch)
        preds = logits.argmax(axis=1)
        labels = batch["labels"]
        for name, metric in self.metrics["val"]:
            metric(preds, labels)
            self.log(
                f"val_{name}",
                metric,
                on_step=False,
                on_epoch=True,
                prog_bar=True,
                logger=True,
            )

        self.log(
            "val_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True
        )
        return preds

    def test_step(self, batch, batch_idx):
        loss, logits = self(batch)
        preds = logits.argmax(axis=1)
        labels = batch["labels"]
        for name, metric in self.metrics["test"]:
            metric(preds, labels)
            self.log(
                f"test_{name}",
                metric,
                on_step=False,
                on_epoch=True,
                prog_bar=True,
                logger=True,
            )

        self.log(
            "test_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True
        )
        return preds

    def configure_optimizers(self):
        """Prepare optimizer and schedule (linear warmup and decay)"""
        model = self.model
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": self.hparams.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.0,
            },
        ]
        optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=self.hparams.lr,
            eps=self.hparams.epsilon,
        )

        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.hparams.num_warmup_steps,
            num_training_steps=self.total_steps,
        )
        scheduler = {"scheduler": scheduler, "interval": "step", "frequency": 1}
        return [optimizer], [scheduler]