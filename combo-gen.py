import random
import string
import json
import time
from faker import Faker

fake = Faker()

print("How many lines do you want to generate?:")
linestogenerate = input()
time1 = time.perf_counter()

lowercase = string.ascii_lowercase
digits = string.digits
password = string.ascii_letters + string.digits + "_" + "." + "_" + "."
email = string.ascii_letters
emailadditive = ["_", "."]

with open("data/emaildomains.json", "r") as domainfile:
    data = domainfile.read()
emaildomains = json.loads(data)

with open("data/firstnames.json", "r") as firstnamefile:
    data = firstnamefile.read()
firstnames = json.loads(data)

with open("data/lastnames.json", "r") as lastnamefile:
    data = lastnamefile.read()
lastnames = json.loads(data)

with open("data/passwords.json", "r") as passfile:
    data = passfile.read()
passwords = json.loads(data)

with open("data/usernames.json", "r") as usernamefile:
    data = usernamefile.read()
usernames = json.loads(data)

combofile = open("generatedcredentials.txt", "a")


def randomName(lower):
    x = random.randint(1, 4)
    if x == 1:
        name = random.choice(firstnames)
    elif x == 2:
        name = random.choice(lastnames)
    elif x == 3:
        name = random.choice(firstnames) + random.choice(lastnames)
    elif x == 4:
        name = fake.name()
    if lower == True:
        name.lower()
    return name.replace(" ", "")


def USER():
    rand = random.randint(1, 3)
    if rand == 1:
        tempuser = randomName(True)
    elif rand == 2:
        return fake.email()
    else:
        tempuser = random.choice(usernames)

    username = ""
    first = True
    additive = False

    for l in tempuser:
        int = random.randint(1, 50)
        if first == True:
            rand = random.randint(1, 20)
            if rand == 1:
                username = l.upper()
            else:
                username = l
            first = False
        else:
            if int <= 2:
                username = username + random.choice(email)
            elif int >= 48 and additive == False:
                username = username + random.choice(emailadditive) + l
                additive = True
            else:
                username = username + l
    return username + "@" + random.choice(emaildomains)


def PASS():
    rand = random.randint(1, 6)
    name = randomName(False)
    if rand == 1:
        return "".join(random.sample(email, random.randint(6, 15)))
    elif rand == 2:
        return name + "".join(random.sample(digits, random.randint(2, 7)))
    elif rand == 3:
        str = ""
        if random.randint(1, 2) == 1:
            name.lower()
        for l in name:
            if random.randint(1, 2) == 1:
                str = str + random.choice(password)
            else:
                str = str + l
        return str
    return random.choice(passwords)


def COMBO():
    return USER() + ":" + PASS()


for i in range(int(linestogenerate)):
    combofile.write(COMBO() + "\n")


time2 = time.perf_counter()
print(linestogenerate + " lines generated in " + str(time2 - time1) + " seconds.")
