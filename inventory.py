import items

class Inventory:

    def __init__(self):
        self.items = []
        self.max_item_count = 32

        for i in range(1):
            self.putin(items.make_test_item("weapon"))
            #self.putin(items.make_test_item("armor"))

    # 집어 넣다.
    def putin(self, a_item):

        current_item_count = len(self.items)
        if current_item_count >= self.max_item_count:
            print("Inventory is full.")
            return

        self.items.append(a_item)

    def get_info(self, item_index):
        a_item = self.items[item_index]

        attr_str = " ".join(a_item.attr_list)
        print("name: {} , attrs: {}".format(a_item.item_name, attr_str))

    # 꺼내다.
    def takeout(self):
        pass

    # 아이템을 삭제한다.
    def discard(self, item_index):

        a_item = self.items[item_index]
        print("{} is deleted.".format(a_item.item_name))
        self.items.remove(a_item)

    def show_list(self):

        if self.is_empty():
            print("Inventory is empty.")
            return

        print("Items:")
        for i, a_item in enumerate(self.items):

            attr_str = " ".join(a_item.attr_list)
            print("({}) {}".format(i+1, a_item.item_name))

    def is_empty(self):
        if len(self.items) == 0:
            return True

        return False

    def is_full(self):
        if len(self.items) >= self.max_item_count:
            return True

        return False
