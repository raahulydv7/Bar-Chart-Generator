datasets = {
    "Fruits": {
        "categories": ["Apples", "Bananas", "Cherries", "Dates"],
        "default_values": [10, 15, 7, 5],
    },
    "Countries": {
        "categories": ["USA", "Canada", "Mexico", "Brazil"],
        "default_values": [30, 20, 25, 10],
    },
    "Products": {
        "categories": ["Laptops", "Tablets", "Smartphones", "Desktops"],
        "default_values": [100, 75, 50, 40],
    },
}


def get_datasets():

    return datasets


def get_dataset_names():

    return list(datasets.keys())


def get_dataset(name):

    return datasets.get(name)


def add_dataset(name, categories, default_values):

    if len(categories) != len(default_values):
        return False

    datasets[name] = {"categories": categories, "default_values": default_values}
    return True
