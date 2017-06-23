

class Item:

    def __init__(self):
        self.item_type = None
        self.item_name = None
        self.attr_list = []
        self.count = 0

    def make(self, item_type, item_name, attribute, a_value):
        self.item_type = item_type
        self.item_name = item_name

        attr_str = attribute + ":" + "{0:+}".format(a_value,)

        self.attr_list.append(attr_str)

    def add_attribute(self, attr_str):
        self.attr_list.append(attr_str)

    def show_me(self):

        print("name:{}, type:{}".format(self.item_name, self.item_type))
        for one in self.attr_list:
            print(one)


def get_attr(attr_str):
    attr_list = attr_str.split(':')
    attr_name = attr_list[0]
    attr_value = int(attr_list[1])          # ValueError의 가능성이 존재

    return attr_name, attr_value


def make_basic_item(item_type):
    an_item = Item()
    if item_type == 'weapon':
        an_item.make("weapon", "fist", "atk", 1)

    elif item_type == "armor":
        an_item.make("armor", "cloth", "hp", 2)

    return an_item


if __name__ == "__main__":

    a_item = Item()
    a_item.make("weapon", "knife", "atk", 10)
    a_item.add_attribute("hp:+10")
    a_item.show_me()