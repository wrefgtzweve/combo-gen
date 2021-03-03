import random
import string
import json
import names
import time

print("How many lines should be generated:")
linestogenerate = input()
time1 = time.perf_counter()

lowercase = string.ascii_lowercase
digits = string.digits
password = string.ascii_letters + string.digits + "_" + "." + "_" + "."
email = string.ascii_letters + string.digits + "!" + "." + "_"

with open("emaildomains.json", "r") as domainfile:
    data = domainfile.read()
emaildomains = json.loads(data)

with open("passwords.json", "r") as passfile:
    data = passfile.read()
passwords = json.loads(data)

combofile = open("generatedcredentials.txt", "a")


def randomName(lower):
    x = random.randint(1, 3)
    if x == 1:
        name = names.get_last_name()
    if x == 2:
        name = names.get_first_name()
    if x == 3:
        name = names.get_full_name()
    if lower == True:
        name.lower()
    return name.replace(" ", "")


def USER():
    tempuser = randomName(True)
    username = ""
    first = True
    for l in tempuser:
        if random.randint(1, 5) == 1 and first == False:
            username = username + random.choice(email)
        else:
            username = username + l
        first = False
    return username.lower() + "@" + random.choice(emaildomains)


def PASS():
    rand = random.randint(1, 4)
    name = randomName(False)
    if rand == 1:
        return "".join(random.sample(email, random.randint(5, 15)))
    if rand == 2:
        return name + "".join(random.sample(digits, random.randint(2, 7)))
    if rand == 3:
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
