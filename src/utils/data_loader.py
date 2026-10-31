from torch.utils.data import DataLoader, Dataset, random_split


def get_dataloader(
    dataset: Dataset,
    batch_size: int,
    shuffle: bool,
    val_split: bool = False,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
):
    size = len(dataset)
    train_size = int(train_ratio * size)
    val_size = int(val_ratio * size) if val_split else 0
    sizes = [train_size, val_size, size - train_size - val_size]
    if not val_split:
        sizes.pop(1)
    splits = random_split(dataset, sizes)

    loaders = {
        "train": DataLoader(splits[0], batch_size=batch_size, shuffle=shuffle),
        "test": DataLoader(splits[-1], batch_size=batch_size, shuffle=False),
    }
    if val_split:
        loaders["val"] = DataLoader(
            splits[1], batch_size=batch_size, shuffle=False
        )
    return loaders
