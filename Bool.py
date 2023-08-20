# обёртка для типа данных bool
class Bool:
    def __init__(self, value=True):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value
