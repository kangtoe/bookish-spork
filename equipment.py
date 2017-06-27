
import items


class Equipment:
    place = ['weapon', 'armor']

    def __init__(self):
        self.place = {}

        for a_place in Equipment.place:
            self.place[a_place] = items.make_basic_item(a_place)

    def equip(self, new_item, a_inventory):

        a_place = new_item.item_type

        a_inventory.takeout(new_item)

        self.unequip(a_place, a_inventory)
        self.place[a_place] = new_item

    # TODO: Inventory에 벗는 장비를 집어 넣어야 된다.
    def unequip(self, a_place, a_inventory):

        a_item = self.place[a_place]
        self.place[a_place] = items.make_basic_item(a_place)

        # 현재 장착된 아이템이 기본 아이템이면 그냥 삭제하자.
        if a_item.item_name != "(none)":
            a_inventory.put_in(a_item)

    def __str__(self):
        return "weapon:{}, armor:{}".format(self.place['weapon'], self.place['armor'])

