class minion(object):
    def __init__(self, name, age):
        self.name = name.title()
        self.age = age

    def update_subject(self, cmd):
        exec(cmd)

def subclass_repr(self):
    article = 'an' if self.type[0] in 'AEIOUY' else 'a'
    return f"Hi! My Name is {self.name} and I'm {article} {self.type}! I have {str(round(self.money, 2))} €"

base_species_metaclass = lambda minion_type, money, base_class=(minion,): \
    type(minion_type, base_class, 
        {
            "type":minion_type.title(), 
            "money":round(money, 2),
            "__repr__":subclass_repr
        }
    )

Human = base_species_metaclass("Human", 5000)
Elf = base_species_metaclass("elf", 10000)


Subject_1 = Human('bob', 33)
Subject_2 = Elf('Alice', 31)

registry = {x:globals()[x] for x in globals() if not x.startswith('_') and isinstance(globals()[x], minion)}

for a_subject, data in registry.items():
    print(f"{a_subject.title()} says: \"{data}\" ")
    diff = sum([i for i in range(1, len(a_subject)+1)])
    command = f"self.money += {diff}"
    data.update_subject(command)
    print(f"{a_subject.title()} will get extra {diff} € ----> cmd: {command} | Result: {data.money} €")

