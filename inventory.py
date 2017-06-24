import items

class Inventory:

    def __init__(self):
        self.items = []
        self.max_item_count = 32

        for i in range(5):
            self.putin(items.make_test_item("weapon"))
            self.putin(items.make_test_item("armor"))

    # 집어 넣다.
    def putin(self, a_item):

        current_item_count = len(self.items)
        if current_item_count >= self.max_item_count:
            print("Inventory is full.")
            return

        self.items.append(a_item)

    # 꺼내다.
    def takeout(self):
        pass

    def show_list(self):

        print("Items:")
        for i, a_item in enumerate(self.items):

            attr_str = " ".join(a_item.attr_list)
            print("({}) name: {}, attrs: {}".format(i+1, a_item.item_name, attr_str))