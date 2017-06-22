
class SkillType:
    # 적군 하나 대상
    type_1 = ['smite', 'smash', '']

    # 아군 하나 대상
    type_2 = ['heal']

    @classmethod
    def get_type(cls, skill_name):
        if skill_name in SkillType.type_1:
            return "type1"
        elif skill_name in SkillType.type_2:
            return "type2"


# 강타: 데미지 2배
def smite(caster, target):

    # TODO: caster가 해당 스킬을 쓸 수 있는지 판단.

    skill_damage = caster.get_atk() * 2
    target.be_attacked(caster.get_name(), skill_damage, "smite")


# smash: 데미지 1.5배
def smash(caster, target):
    # TODO: caster가 해당 스킬을 쓸 수 있는지 판단.

    skill_damage = caster.get_atk() * 1.5
    target.be_attacked(caster.get_name(), skill_damage, "smash")



# 치유: hp 회복
def heal(caster, target):
    skill_damage = caster.get_atk()
    target.heal_system(caster.get_name(), skill_damage)
