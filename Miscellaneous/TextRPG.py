import random

'''Player Stats'''
Attack = 10
Defence = 10
Health = 20
Restoration = 5


'''MonsterBase'''
MAttack = 0
MDefence = 0
MHealth = 0

i = 0
Defeated = 0

MonsterList = ['Elf','Orc','Troll','Wolf','Zombie','Skeleton','Ghost','Ghoul']

while Health > 0:
    while i != 1:
        if Defeated <= 5:
            MAttack = random.randint(1,5)
            MHealth = random.randint(10,40)
            Name = MonsterList[random.randint(0,7)]
            i = 1
            print("A(n)", Name, "approaches!")
        elif Defeated > 5:
            MAttack = random.randint(5,15)
            MHealth = random.randint(15,50)
            Name = MonsterList[random.randint(1, 3)]
            i = 1
            print("A(n)", Name, "approaches!")
    print("Attack Power: " , MAttack)
    print("Health: " , MHealth)
    choice = input("\nDo you wish to attack? y/n \n")
    if choice == 'y':
        MHealth -= Attack
        print("\nYou hit the", Name, "for", Attack, "damage!")
        if MHealth <= 0:
            print("Monster Defeated!")
            Defeated += 1
            StatChoice = input("Do you wish to heal? [H] or improve a stat [A] or [R]")
            if StatChoice.upper() == 'H':
                Health += Restoration
                print("\n\nYour health is now at: ", Health)
                i = 0
            elif StatChoice.upper() == 'A':
                Attack += random.randint(1,5)
                print("\n\nYour attack is now at: ", Attack)
                i = 0
            elif StatChoice.upper() == 'R':
                Restoration += random.randint(1,5)
                print("\n\nYour restoration stat is now at: ", Restoration)
                i = 0
        else:
            Health -= MAttack
            print("The monster hit you for", MAttack, "points of damage")
            print("\nPlayer health :" , Health, "\n")
    elif choice == 'n':
        EscapeChance = random.randint(1,2)
        if EscapeChance == 1:
            print("You failed to run from the monster!")
            Health -= MAttack
            print("The monster hit you for" ,MAttack, "points of damage")
            print("\nPlayer health :", Health, "\n")
        else:
            print("You escaped!")
            i = 0
    elif choice == 'attack':
        print("Your attack is: ", Attack)
    elif choice == 'health':
        print("Your health is: ", Health)


print("You were slain in battle,")
print("Your final stats were")
print("Total Monsters Defeated: ", Defeated)



