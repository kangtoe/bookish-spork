

# 강타: 데미지 2배
def smite(caster, target):

    # TODO: caster가 해당 스킬을 쓸 수 있는지 판단.

    skill_damage = caster.get_atk() * 2
    target.be_attacked(caster.get_name(), skill_damage, "smite")



# 치유: hp 회복
def heal(caster, target):
    skill_damage = caster.get_atk()
    target.heal_system(caster.get_name(), skill_damage)
