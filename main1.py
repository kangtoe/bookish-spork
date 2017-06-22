
import skills


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

    def belong(self, party):
        self.party = party

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

            print("\n{} Turn: Now is your turn. (battle=1, retreat=2):".format(GM.turn))
            a = input("> ")
            if a == '1':
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
                attacker = GM.user_team.characters[choice_value-1]


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
        member.belong(self)

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

    # chracter가 죽을 때 team에 자기의 죽음을 알린다.
    def die_member(self, a_characer):

        self.characters.remove(a_characer)
        self.lives = len(self.characters)

        # 전멸
        # TODO: 전멸 처리
        if self.lives == 0:
            pass


def main():

    GM.deploy()
    GM.start_fight()

main()

# next: item구현
# equipment를 우선적으로 구현한다.
# 장비의 종류는 크게 무기, 방어구,장신구로 나뉜다.
# 먼저 atk+10d의 도검과 atk+20의 도끼를 만들어 장착해본다.
