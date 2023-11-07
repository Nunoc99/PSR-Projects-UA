#!/usr/bin/env python3



class Person():
    def __init__(self, name, age, civil_state):#o construtor que é chamado sempre que se instancia um objeto ou classe
        self.name = name
        self.age = age
        self.civil_state = civil_state
        self.spouse = None

    def congratulations(self):
        print("Congratulations" + self.name)
        self.age += 1

    def marry(self, partner):
        if not self.civil_state == "single":
            print("Perhaps this is not a good idea.")
            return
        
        if not partner.civil_state == "single":
            print("There are better options out there.")
            return

        self.spouse = partner.name
        self.civil_state = "Married"
        partner.spouse = self.name
        partner.civil_state = "Married"

    def __str__(self):
        text = "I am " + self.name + " " + str(self.age) + " years old, " + self.civil_state
        return text


def main():
    p1 = Person(name = "João", age = 33, civil_state = "Single")
    p2 = Person(name = "Maria", age = 34, civil_state = "Single")
    
    print(p1)
    print(p2)
    p1.congratulations()

    p1.marry(p2)
    print(p1)
    print(p2)

   

if __name__ == "__main__":
    main()





#def main(): COMO SERIA SEM CLASSES...
    #nome1 = "Joao"
    #idade1 = 33
    #estado_civil1 = "solteiro"

    #nome2 = "Maria"
    #idade2 = 34
    #estado_civil2 = "solteira"

    #conjugue1 = "Maria"
    #conjugue2 = "João"

    #estado_civil1 = "Casado"
    #estado_civil2 = "Casado"







