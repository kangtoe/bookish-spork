
import skills


class SkillType:
    # 적군 하나 대상
    type_1 = ['smite', '', '']

    # 아군 하나 대상
    type_2 = ['heal']

    @classmethod
    def get_type(cls, skill_name):
        if skill_name in SkillType.type_1:
            return "type1"
        elif skill_name in SkillType.type_2:
            return "type2"


class RpgChararcter:

    def __init__(self, name,  hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.alive = True
        self.max_hp = hp
        self.skills = ['heal', 'smite']

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

        print("Use : " + " ".join(str_skills))

        sk = input("> ")

        return int(sk)

    def die(self):
        self.alive = False
        print("{} is dead".format(self.get_name()))


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

        team.pickone_members(title)

        a = input("> ")
        choose_one_index = int(a) - 1

        return team.characters[choose_one_index]

    # 적군중 한명을 공격하고자 고른다.
    @classmethod
    def pickone_enemy(cls):

        return GM.pickone(GM.enemies)

    @classmethod
    def pickone_member(cls):

        return GM.pickone(GM.user_team)

    @classmethod
    def fight(cls, attacker, attacked):

        # 살아 있는지 검사
        # TODO: 죽으면 공격 대상에서 제외.
        if not attacker.is_alive():
            return

        attacker_atk = attacker.get_atk()
        attacked.be_attacked(attacker.get_name(), attacker_atk)
        attacked.get_hp()


    @classmethod
    def start_fight(cls):
        # 공격할지 물어보자

        GM.turn = 1

        while True:

            # TODO: 바른 답변인지 검증 필요.
            print("\n{} Turn: Now is your turn. (battle=1, retreat=2):".format(GM.turn))
            a = input("> ")
            if a == '1':
                GM.turn += 1

                GM.user_team.pickone_members("Member to act: ")
                ask_str = "> "

                result = input(ask_str)
                choice_index = int(result)

                # TODO: 바른 답변인지 검증 필요.

                # 누가 싸우나?
                attacker = GM.user_team.characters[choice_index-1]

                # 뭐 할지 물어보자.
                print("{} act: (attack='a', skill='s')".format(attacker.get_name()))
                choice_act = input("> ")

                if choice_act == 's':

                    sk = attacker.choose_skill()
                    available_skills = attacker.get_skills()

                    skill_name = available_skills[sk - 1]

                    sk_type = SkillType.get_type(skill_name)

                    # 적군 대상
                    if sk_type == 'type1':
                        target = GM.pickone_enemy()
                    elif sk_type == 'type2':
                        target = GM.pickone_member()

                    skill_method = getattr(skills, skill_name)
                    skill_method(attacker, target)

            elif a == '2':
                print('you retreated')
                break

            else:
                pass


class Team:

    def __init__(self):

        self.characters = []
        self.lives = 0

    def add(self, member):

        self.characters.append(member)
        self.lives = len(self.characters)

       #print(self.lives)

    def show_members(self):

        # 멤버들을 보여주자.

        print("My Party Members:")
        i = 0
        for one in self.characters:
            i += 1
            print("({}) {}: hp: {}. atk: {}".format(i, one.get_name(), one.get_hp(), one.get_atk()))

    # 뭔가 하기 위해 팀에서 한명을 고르자.
    def pickone_members(self, title):

        print(title)

        for i, one in enumerate(self.characters):
            print("({}) name: {}, hp: {}. atk: {}".format(i+1, one.get_name(), one.get_hp(), one.get_atk()))


def main():

    GM.deploy()
    GM.start_fight()

main()

# next: item구현
# equipment를 우선적으로 구현한다.
# 장비의 종류는 크게 무기, 방어구,장신구로 나뉜다.
# 먼저 atk+10d의 도검과 atk+20의 도끼를 만들어 장착해본다.
