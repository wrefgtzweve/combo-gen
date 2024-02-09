import random
import string
import json
import time
import datetime
import sys
from faker import Faker

fake = Faker()

linestogenerate = sys.argv.pop() if len(sys.argv) > 1 else ""
if linestogenerate == "":
    print("No amount of lines to generate specified, defaulting to 50000")
    linestogenerate = 50000

time1 = time.perf_counter()

lowercase = string.ascii_lowercase
digits = string.digits
password = string.ascii_letters + string.digits + "_" + "." + "_" + "."
email = string.ascii_letters
emailadditive = ["_", "."]

with open("data/emaildomains.json", "r", encoding="utf-8") as domainfile:
    data = domainfile.read()
emaildomains = json.loads(data)

with open("data/firstnames.json", "r", encoding="utf-8") as firstnamefile:
    data = firstnamefile.read()
firstnames = json.loads(data)

with open("data/lastnames.json", "r", encoding="utf-8") as lastnamefile:
    data = lastnamefile.read()
lastnames = json.loads(data)

with open("data/passwords.json", "r", encoding="utf-8") as passfile:
    data = passfile.read()
passwords = json.loads(data)

with open("data/usernames.json", "r", encoding="utf-8") as usernamefile:
    data = usernamefile.read()
usernames = json.loads(data)

combofile = open(
    "generatedcredentials"
    + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    + ".txt",
    "a",
    encoding="utf-8",
)


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
    if lower:
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

    for letter in tempuser:
        int = random.randint(1, 50)
        if first:
            rand = random.randint(1, 20)
            if rand == 1:
                username = letter.upper()
            else:
                username = letter
            first = False
        else:
            if int <= 2:
                username = username + random.choice(email)
            elif int >= 48 and not additive:
                username = username + random.choice(emailadditive) + letter
                additive = True
            else:
                username = username + letter
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
        for letter in name:
            if random.randint(1, 2) == 1:
                str = str + random.choice(password)
            else:
                str = str + letter
        return str
    return random.choice(passwords)


def COMBO():
    line = USER() + ":" + PASS()
    combofile.write(line + "\n")


for i in range(int(linestogenerate)):
    COMBO()

time2 = time.perf_counter()
print(str(linestogenerate) + " lines generated in " + str(round((time2 - time1), 3)) + " seconds.")
