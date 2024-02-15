package main

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

//go:embed data/emaildomains.json
var emaildomains []byte
var emailDomainList []string

//go:embed data/firstnames.json
var firstnames []byte
var firstNameList []string

//go:embed data/lastnames.json
var lastnames []byte
var lastNameList []string

//go:embed data/passwords.json
var passwords []byte
var passwordList []string

//go:embed data/usernames.json
var usernames []byte
var usernameList []string

var emailadditive = []string{".", "_", "-"}
var letterList = []string{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "x", "y", "z"}
var digitList = []string{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
var passwordCharList = []string{"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", ";", ":", "'", "\"", ",", "<", ".", ">", "/", "?", "~"}

func randomName(lower bool) string {
	n := rand.Intn(2)
	name := ""

	if n == 0 {
		name = firstNameList[rand.Intn(len(firstNameList))]
	} else if n == 1 {
		name = lastNameList[rand.Intn(len(lastNameList))]
	} else if n == 2 {
		name = firstNameList[rand.Intn(len(firstNameList))] + lastNameList[rand.Intn(len(lastNameList))]
	}

	if lower {
		name = strings.ToLower(name)
	}

	return name
}

func getUser() string {
	n := rand.Intn(2)
	name := ""

	if n == 0 {
		name = randomName(true)
	} else if n == 1 {
		name = usernameList[rand.Intn(len(usernameList))]
	}

	userName := ""
	isFirst := true
	for i := 0; i < len(name); i++ {
		rnd := rand.Intn(50)
		letter := string(name[i])
		if rnd <= 2 {
			userName = userName + letterList[rand.Intn(len(letterList))] + letter
		} else if rnd >= 48 && !isFirst {
			userName = userName + emailadditive[rand.Intn(len(emailadditive))] + letter
		} else {
			userName = userName + letter
		}
		isFirst = false
	}

	return userName + "@" + emailDomainList[rand.Intn(len(emailDomainList))]
}

func getPassword() string {
	rnd := rand.Intn(5)
	name := randomName(false)

	if rnd == 0 {
		pw := ""
		for i := 0; i < rand.Intn(11)+6; i++ {
			pw = pw + letterList[rand.Intn(len(letterList))]
		}
		return pw
	} else if rnd == 1 {
		pw := ""
		for i := 0; i < rand.Intn(11)+6; i++ {
			pw = pw + digitList[rand.Intn(len(digitList))]
		}
		return pw
	} else if rnd == 2 {
		pw := ""
		if rand.Intn(2) == 0 {
			pw = strings.ToLower(name)
		}

		str := ""
		for i := 0; i < len(pw); i++ {
			if rand.Intn(2) == 0 {
				if rand.Intn(6) == 0 {
					str = str + passwordCharList[rand.Intn(len(passwordCharList))]
				} else {
					str = str + letterList[rand.Intn(len(letterList))]
				}
			} else {
				str = str + string(pw[i])
			}
		}

		return str
	}

	return passwordList[rand.Intn(len(passwordList))]
}

func getCombo() string {
	return getUser() + ":" + getPassword()
}

func main() {
	starTime := time.Now()
	count := 0
	if len(os.Args) < 2 {
		fmt.Println("No count provided, using default count of 50000")
		count = 50000
	} else {
		c, err := strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Println("Invalid count provided, using default count of 50000")
			count = 50000
		}

		fmt.Println("Count provided: ", c)
		count = c
	}

	json.Unmarshal(emaildomains, &emailDomainList)
	json.Unmarshal(firstnames, &firstNameList)
	json.Unmarshal(lastnames, &lastNameList)
	json.Unmarshal(passwords, &passwordList)
	json.Unmarshal(usernames, &usernameList)

	if _, err := os.Stat("output"); os.IsNotExist(err) {
		os.Mkdir("output", 0755)
	}

	newFile, error := os.Create("output/combos-" + time.Now().Format("2006-01-02-15-04-05") + ".txt")
	if error != nil {
		fmt.Println("Error creating file")
		return
	}

	defer newFile.Close()

	var wg sync.WaitGroup
	wg.Add(300)
	generated := 0

	for i := 0; i < 300; i++ {
		go func() {
			threadBuffer := ""
			threadBufferCount := 0
			for count > generated {
				combo := getCombo()

				threadBuffer = threadBuffer + combo + "\n"

				threadBufferCount++
				if threadBufferCount >= 10000 {
					newFile.WriteString(threadBuffer)
					threadBuffer = ""
					threadBufferCount = 0
				}

				generated++
			}

			if threadBuffer != "" {
				newFile.WriteString(threadBuffer)
			}
			wg.Done()
		}()
	}
	wg.Wait()

	fmt.Println("Combos generated successfully")
	fmt.Printf("Time taken: %.2f seconds", time.Since(starTime).Seconds())
}
