class Generator:
    def __init__(self, dict):
        self.dict = dict

    def generate(self):
        xml = ""
        for key in self.dict.keys():
            xml += self.__generate_node(key)
        return xml

    def __generate_node(self, key):
        open_tag = "<" + key + ">"
        close_tag = "</" + key + ">"

        value = self.dict[key]

        if type(value) == str:
            return open_tag + value + close_tag
