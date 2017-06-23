
import items


class Equipment:
    place = ['weapon', 'armor']

    def __init__(self):
        self.place = {}

        for a_place in Equipment.place:
            self.place[a_place] = items.make_basic_item(a_place)

    def equip(self, new_item):

        a_place = new_item.item_type
        self.unequip(a_place)
        self.place[a_place] = new_item

    # TODO: Inventory에 벗는 장비를 집어 넣어야 된다.
    def unequip(self, a_place):
        pass

