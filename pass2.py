import nltk

filemntc = open("mntc.txt").readlines()
mntc =[]
for line in filemntc:
    lineToken = nltk.word_tokenize(line)
    # print(lineToken)
    mntc.append(lineToken[0])
    mntc.append(lineToken[1])
# print(mntc)

filearg = open("arg.txt").readlines()
arg = []
for line in filearg:
    lineToken = nltk.word_tokenize(line)
    arg.append(lineToken[1])
    arg.append("#" + lineToken[3])
# print(arg)

# mntclen = len(mntc)
# print(mntc)
# if "M1" in mntc:
#     print("true")
# else:
#     print("false")

filemdtc = open("mdtc.txt").readlines()
fileIC = open("intermediateCode.txt").readlines()
fileP2 = open("pass2.txt","w")
for line in fileIC:
    newline = line
    lineToken = nltk.word_tokenize(line)

    if lineToken[0] in mntc:
        mntcindex = mntc.index(lineToken[0]) + 1
        mdtcindex = int(mntc[mntcindex])
        # print(filemdtc[mdtcindex])
        
        
        argsToken = nltk.word_tokenize(filemdtc[mdtcindex])
        macroarg = []
        previous = argsToken[0]
        #this for loop is to initialize macrotoken 
        for token in argsToken:
            if previous == "&":
                if "=" in token:
                    temparg = [None, None]
                    temp = ""
                    
                    for alphabate in token:
                        if alphabate == "=":
                            temparg[0] = temp
                            temp = ""
                        else:
                            temp += alphabate
                    
                    temparg[1] = temp

                    macroarg.append(temparg)

                else :
                    macroarg.append([token , None])
            
            previous = token
        print(macroarg)

        print(lineToken)
        #this part is to associate args with there values
        previous = lineToken[0]
        currentargindex = 0
        macrolen = len(macroarg)
        for token in lineToken:
            if (previous in mntc or previous == ",") and previous != "&" and previous != token and token != "&":
                print(currentargindex)
                if macroarg[currentargindex][1] != None:
                    while macroarg[currentargindex][1] != None:
                        currentargindex += 1
                    
                macroarg[currentargindex][1] = token
                print(macroarg)
                currentargindex += 1
            
            if previous == "&":
                temparg = ""
                tempval = ""
                flag = 0
                for i in token:
                    if i != "=" and flag == 0:
                        temparg += i
                    elif i == "=":
                        flag = 1
                    else:
                        tempval += i

                index = 0
                for i in macroarg:
                    if i[0] == temparg:
                        macroarg[index][1] = tempval
                        break
                    
                    index += 1
                
                print(macroarg)
            previous = token
        
        print(arg)
        mdtcindex += 1
        while "MEND" not in filemdtc[mdtcindex]:
            newmdtcline = filemdtc[mdtcindex]
            mdtclinetoken = nltk.word_tokenize(filemdtc[mdtcindex])

            for i in macroarg:
                index = arg.index(i[0]) + 1
                newmdtcline = newmdtcline.replace(arg[index], i[1])

            fileP2.write(newmdtcline)
            mdtcindex += 1

    else:
        fileP2.write(newline)    


            

