
import skills
import items
import equipment
import inventory


# 타입핑된 값에서 안전하게 숫자 추출
def safe_to_int(a_type_value):

    try:
        rtn_int = int(a_type_value)
    except ValueError:
        return None

    return rtn_int

class RpgChararcter:

    def __init__(self, name,  hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.alive = True
        self.max_hp = hp
        self.skills = ['heal', 'smite', 'smash']
        self.party = None
        self.equipment = equipment.Equipment()
        self.inventory = None

        self.recalc_attr()

    def __str__(self):
        return "{}, hp:{}/{}, atk:{} equip:[{}]".format(self.name, self.hp, self.max_hp, self.atk, self.equipment)

    #def __repr__(self):
    #    print("{}, hp:{}/{}, atk:{}".format(self.name, self.hp, self.max_hp, self.atk))

    # 장비를 장착한다.
    def equip(self, a_item):
        self.equipment.equip(a_item, self.inventory)
        self.recalc_attr()

    def unequip(self, a_place):
        self.equipment.unequip(a_place, self.inventory)

    # Equipment에 의해 attribute의 재평가
    def recalc_attr(self):
        for a_place in equipment.Equipment.place:

            if self.equipment.place[a_place]:
                my_equip = self.equipment.place[a_place]

                for a in my_equip.attr_list:
                    self.set_attr(a)

    # attr_str을 받아서 캐릭터의 atk와 hp를 조정한다.
    # ex) "atk:+10" -> "atk" 10 증가
    def set_attr(self, attr_str):
        (attr_name, attr_value) = items.get_attr(attr_str)
        if attr_name == "atk":
            self.atk += attr_value
        elif attr_name == "hp":
            self.max_hp += attr_value

    def get_name(self):
        return self.name

    def get_atk(self):
        return self.atk

    def get_hp(self):

        # name = self.get_name()
        # rtn_str = "{}'s hp is {}".format(name, self.hp)
        # print(rtn_str)

        return self.hp

    # caster.get_name(), skill_damage, "heal"
    def heal_system(self, caster_name, heal_value):
        self.hp += heal_value
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        print("{} is recovered by {}. Now hp is {}.".format(self.get_name(), heal_value, self.get_hp()))

    def be_attacked(self, attacker_name, damaged_value, skill_name="attack"):
        if not self.alive:
            # already dead

            print("{} is already dead".format(self.get_name()))
            return

        self.hp = self.hp - damaged_value
        if self.hp <= 0:
            self.hp = 0
            self.die()

        name = self.get_name()

        if skill_name == "attack":
            rtn_str = "{} hits {}.".format(attacker_name, name)
        else:
            rtn_str = "{} use {} to {}.".format(attacker_name, skill_name, name)

        rtn_str += " {} is damaged by {}. Now hp is {}.".format(name, damaged_value, self.get_hp())
        print(rtn_str)

    def is_alive(self):
        return self.alive

    def get_skills(self):
        return self.skills

    def choose_skill(self):

        str_skills = []
        for i, one_skill in enumerate(self.get_skills()):
            a_str = "({}) {}".format(i+1, one_skill)
            str_skills.append(a_str)

        max_index = len(self.get_skills())

        while True:
            print("Use : " + " ".join(str_skills))

            sk = input("> ")

            # sk값이 index에 합당한지 검사하자.
            selected_value = safe_to_int(sk)
            if selected_value and 0 < selected_value <= max_index:
                return selected_value

    # 소속 및 Team의 요소에 연결할 내용이 있다면 여기서 하자.
    def belong(self, party):
        self.party = party
        self.link_inventory(self.party)

    # Team의 Inventory를 연결한다.
    def link_inventory(self, party):
        self.inventory = party.inventory

    def die(self):
        self.alive = False
        print("{} is dead".format(self.get_name()))

        # team에 죽음을 알리자.
        self.party.die_member(self)


class GM:
    # 캐릭터들 list
    user_team = None
    enemies = None
    turn = 0

    def __init__(self):
        pass

    @classmethod
    def deploy(cls):

        my_party = Team()

        joe = RpgChararcter('joe', 100, 10)
        jane = RpgChararcter('jane', 90, 8)

        my_party.add(joe)
        my_party.add(jane)

        enemies = Team()

        orc = RpgChararcter('orc', 100, 10)
        tiger = RpgChararcter('tiger', 120, 8)

        enemies.add(orc)
        enemies.add(tiger)

        GM.user_team = my_party
        GM.enemies = enemies

    @classmethod
    def pickone(cls, team):

        if team == GM.enemies:
            title = "Targets:"
        else:
            title = "Members:"

        max_team_member = team.lives
        while True:
            team.pickone_members(title)

            a = input("> ")

            a_value = safe_to_int(a)

            if a_value and 0 < a_value <= max_team_member:
                return team.characters[a_value-1]

    # 적군중 한명을 공격하고자 고른다.
    @classmethod
    def pickone_enemy(cls):

        return GM.pickone(GM.enemies)

    @classmethod
    def pickone_member(cls):

        return GM.pickone(GM.user_team)

    @classmethod
    def fight(cls, attacker, target):

        # 살아 있는지 검사
        # TODO: 죽으면 공격 대상에서 제외.
        if not attacker.is_alive():
            return

        attacker_atk = attacker.get_atk()
        target.be_attacked(attacker.get_name(), attacker_atk)
        target.get_hp()


    @classmethod
    def start_fight(cls):
        # 공격할지 물어보자

        GM.turn = 1

        while True:

            print("\n{} Turn: Now is your turn. (battle=1, retreat=2, inventory=3, character=4):".format(GM.turn))
            a = input("> ")

            # battle 선택
            if a == '1':
                GM.menu_battle()

            # retreat 선택
            elif a == '2':
                print('you retreated')
                break

            # Inventory 메뉴 선택
            elif a == '3':
                GM.menu_inventory()

            # Character 메뉴 선택
            elif a == '4':
                GM.menu_chracter()

            else:
                pass

    @classmethod
    def menu_battle(cls):
        GM.turn += 1

        max_member = GM.user_team.lives
        while True:
            GM.user_team.pickone_members("Member to act: ")
            ask_str = "> "

            result = input(ask_str)
            choice_value = safe_to_int(result)

            if choice_value and 0 < choice_value <= max_member:
                break

        # 누가 싸우나?
        attacker = GM.user_team.characters[choice_value - 1]

        while True:
            # 뭐 할지 물어보자.
            print("{} act: (attack='a', skill='s')".format(attacker.get_name()))
            choice_act = input("> ")

            # skill
            if choice_act == 's':

                sk = attacker.choose_skill()
                available_skills = attacker.get_skills()

                skill_name = available_skills[sk - 1]

                sk_type = skills.SkillType.get_type(skill_name)

                # 적군 대상
                if sk_type == 'type1':
                    target = GM.pickone_enemy()
                elif sk_type == 'type2':
                    target = GM.pickone_member()

                skill_method = getattr(skills, skill_name)
                skill_method(attacker, target)
                break
            # attack
            elif choice_act == 'a':
                target = GM.pickone_enemy()
                GM.fight(attacker, target)
                break

    @classmethod
    def menu_inventory(cls):
        GM.user_team.show_inventory()

        # 먼저 inventory가 비어 있는지 검사하자.
        if GM.user_team.inventory.is_empty():
            return

        while True:
            print("Choose an item: ")
            a = input("> ")

            a_int = safe_to_int(a)

            if a_int is None:
                continue

            a_index = a_int - 1
            max_index = len(GM.user_team.inventory.items)
            if 0 <= a_index < max_index:
                break

        # 정보를 보여주고 장착/삭제 등을 선택하게 한다.
        while True:
            # 아이템 정보를 자세히 보여준다.
            a_item = GM.user_team.inventory.get_info(a_index)

            print("(equip=1, use=2, discard=3)")
            a = input("> ")

            if a == '1':

                my_team = GM.user_team
                my_inventory = my_team.inventory

                # 누구에게 equip 할지 골라야 된다.
                a_char = GM.pickone(my_team)
                my_equipment = a_char.equipment

                a_char.equip(a_item)

                print(a_char)
                break
            elif a == '2':
                # 누구에게 use 할지 골라야 된다
                break
            elif a == '3':
                GM.user_team.inventory.discard(a_index)
                break
            else:
                pass

    @classmethod
    def menu_chracter(cls):

        while True:
            GM.user_team.pickone_members("Member to manage: ")
            ask_str = "> "

            result = input(ask_str)
            choice_value = safe_to_int(result)
            max_member = GM.user_team.lives

            if choice_value and 0 < choice_value <= max_member:
                break

        # 선택된 캐릭터
        a_man = GM.user_team.characters[choice_value - 1]

        # 정보를 보여주고 장착/삭제 등을 선택하게 한다.
        while True:
            # Equipment 정보를 보여준다.
            a_man.equipment.show_equipment()

            ask_str = "> "

            result = input(ask_str)

            int_result = safe_to_int(result)

            max_result = len(a_man.equipment.place)
            if choice_value and 0 < int_result <= max_result:
                break

        safe_to_int(result)

        equip_place_index = int_result-1
        a_place = equipment.Equipment.place[equip_place_index]
        a_item = a_man.equipment.place[a_place]
        #
        print("Item to manage: {}".format(a_item.item_name))

        while True:
            print("(change=1, unequip=2, discard=3):")
            ask_str = "> "

            result = input(ask_str)

            # change
            if result == '1':

                # TODO: Inventory에서 같은 유형만 보여준다.
                break
            # unequip
            elif result == '2':
                pass
                break

            # discard
            elif result == '3':
                pass
                break

            else:
                pass


    @classmethod
    def menu_character_equip(cls):

        while True:

            if True:
                pass


class Team:

    def __init__(self):

        self.characters = []
        self.lives = 0
        self.inventory = inventory.Inventory()

    def add(self, member):

        self.characters.append(member)
        self.lives = len(self.characters)

        # 연결이 필요한 요소들을 연결시킨다.
        # ex) 해당 inventory 연결, 팀하고 캐릭터를 연결
        member.belong(self)

       #print(self.lives)

    def show_members(self):

        # 멤버들을 보여주자.

        print("My Party Members:")
        i = 0
        for one in self.characters:
            i += 1
            print("({}) {}: hp:{}/{}, atk:{}, equip:[{}]".format(
                i, one.get_name(), one.get_hp(), one.max_hp, one.get_atk(), one.equipment))

    # 뭔가 하기 위해 팀에서 한명을 고르자.
    def pickone_members(self, title):

        print(title)

        for i, one in enumerate(self.characters):
            print("({}) name:{}, hp:{}/{}, atk:{}, equip:[{}]".format(
                i+1, one.get_name(), one.get_hp(), one.max_hp, one.get_atk(), one.equipment))

    # chracter가 죽을 때 team에 자기의 죽음을 알린다.
    def die_member(self, a_characer):

        self.characters.remove(a_characer)
        self.lives = len(self.characters)

        # 전멸
        # TODO: 전멸 처리
        if self.lives == 0:
            print("You Lose!")

    def show_inventory(self):
        self.inventory.show_list()

def main():

    GM.deploy()
    GM.start_fight()

main()


# 먼저 atk+10d의 도검과 atk+20의 도끼를 만들어 장착해본다.
