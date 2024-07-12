from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    def __init__(self):
        self.includes = []
        self.available_includes = []
        self.default_includes = []

    @abstractmethod
    def transform(self, item):
        pass

    def include(self, includes: list[str]):
        for include in includes:
            if include in self.available_includes:
                self.includes.append(include)
        return self

    def transform_with_includes(self, item):
        data = self.transform(item)
        for include in list(set(self.includes + self.default_includes)):
            func = getattr(self, 'include_' + include)
            setattr(data, include, func(item))
        return data

    def item(self, data, transformer):
        if data is None:
            return None
        return transformer.transform_with_includes(data)

    def collection(self, data, transformer):
        if data is None:
            return None
        return [self.item(el, transformer) for el in data]


def transform(data, transformer: BaseTransformer):
    """
    Transforms the data with the given transformer
    :param data: data to transform: model, list, null or paginator? todo paginator
    :param transformer:
    :return: returns none, dict, or array of dicts
    """
    if data is None:
        return None
    if isinstance(data, list):
        return [transformer.transform_with_includes(item) for item in data if item]
    if False:
        pass  # pagination stuff?
    # model
    return transformer.transform_with_includes(data)
