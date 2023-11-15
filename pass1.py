import nltk

mi = open("macro_input.txt").readlines()
tempMacro = open("mdtc.txt","w")
intermediateCode = open("intermediateCode.txt","w")
mntc = open("mntc.txt","w")
arg = open("arg.txt","w")
# print(mi)

macroFlag = 0
mntcCount = 1
miIndex = 0
argCount = 0
args = []
previousLine = ""
for line in mi:
    # print(line + " " + str(miIndex))
    if "MACRO" in previousLine:
        macroFlag = 1
        
        tempMacro.write(previousLine)
        tempMacro.write(line)
        
        
        # This part of code is for creating arguments table
        lineToken = nltk.word_tokenize(mi[miIndex])
        previous = lineToken[0]
        for word in lineToken:
            if previous == '&':
                if "=" in word:
                    eqArg = ""
                    for alphabate in word:
                        if alphabate == "=":
                            break
                        else:
                            eqArg += alphabate
                    arg.write("&" + eqArg + " " + "#" + str(argCount) + "\n")
                    args.append(eqArg)
                else:    
                    arg.write("&" + word + " " + "#" + str(argCount) + "\n")
                    args.append(word)
                
                argCount += 1
            
            previous = word
        
        macroName = lineToken[0]
        mntc.write(macroName + " " + str(mntcCount) + "\n")
        previousLine = line
        miIndex += 1
        mntcCount += 2
        # tempMacro.write(line)
        continue

    if "MEND" in line:
        tempMacro.write(line)
        macroFlag = 0
        # tempMacro.write(line)
        previousLine = line
        miIndex += 1
        mntcCount += 1
        continue

    if macroFlag == 1:
        newLine = line
        # tempMacro.write(line)
        lineToken = nltk.word_tokenize(line)
        
        #this part of code is to replace the arguments name with there index
        for word in lineToken:
            if word in args:
                index = args.index(word)
                newLine = newLine.replace("&" + word, "#" + str(index))
    
        tempMacro.write(newLine)
        mntcCount += 1
    else :
        if "MACRO" not in line:
            intermediateCode.write(line)

    previousLine = line
    miIndex += 1

tempMacro.close()
intermediateCode.close()
mntc.close()
arg.close()



    