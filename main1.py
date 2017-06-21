
import skills

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

    def heal(self, heal_value):
        self.hp += heal_value
        if self.hp > self.max_hp:
            self.hp = self.max_hp

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
            rtn_str = "{} hits {}. {} is damaged by {}".format(attacker_name, name, name, damaged_value)
        else:
            rtn_str = "{} use {} to {}. {} is damaged by {}".format(attacker_name, skill_name, name, name, damaged_value)

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

    # 적군중 한명을 공격하고자 고른다.
    @classmethod
    def pickone_enemy(cls):

        alist = []
        for i, one in enumerate(GM.enemies.characters):
            astr = "({}) {}".format(i+1, one.get_name())
            alist.append(astr)

        print("Targets: " + " ".join(alist))
        a = input("> ")

        choose_one_index = int(a) - 1

        return GM.enemies.characters[choose_one_index]


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

                    target = GM.pickone_enemy()

                    skill_name = available_skills[sk - 1]
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

    # 뭔가 하기 위해 우리팀에서 한명을 고르자.
    def pickone_members(self, title):

        print(title)

        for i, one in enumerate(self.characters):
            print("({}) {}: hp: {}. atk: {}".format(i+1, one.get_name(), one.get_hp(), one.get_atk()))


def main():

    GM.deploy()
    GM.start_fight()

main()

# next?
