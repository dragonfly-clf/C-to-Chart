KeyHong = []

def Hong(List):#Define
    AnsList = []
    Anslist = []
    Old = []
    New = []
    sum = 0

    for String in List:
        hong = String.find('#define')
        if (hong == -1):
            AnsList.append(String)
            continue
        String = String[hong+8:]
        Space = String.find(' ')
        Old.append(String[:Space])
        New.append(String[Space+1:])
        sum += 1

    for String in AnsList:
        cnt = 0
        for Sa in Old:
            if (sum > cnt):
                Sc = New[cnt]
                cnt += 1
                String = String.replace(Sa, Sc)
        Anslist.append(String)

    return Anslist


def DeleteNote(List):
    Left = 0#1->一个/, 2->双边注释前半边， 3->双边注释后半边*
    AnsList = []
    Mark = 0#标注是不是仍然是双边注释
    for String in List:
        LeftNumber = 0
        for word in String:
            LeftNumber += 1

            if (Mark == 1):
                String = String[0: LeftNumber-1] + String[LeftNumber:]
                LeftNumber -= 1
                if (Left == 3 and word == '/'):
                    Mark = 0
                    Left = 0
                if (word == '*'):
                    Left = 3
                continue

            if (Left == 0 and word == '/'):
                Left = 1
                continue

            if (word == '/' and Left == 1):#说明是单边的注释
                String = String[0: LeftNumber-2]
                Left = 0
                break

            if (word == '*' and Left == 1):#说明是双边注释的前半边
                Mark = 1
                Left = 2
                String = String[0: LeftNumber-2] + String[LeftNumber:]
                LeftNumber -= 2
                continue

            if (Left == 1 and word != '/'):#错认了
                Left = 0
                continue

        AnsList.append(String)
    return AnsList


if __name__=='__main__':
    Result = []
    filename = input("Please input the path:")
    Filename = open(filename)
    for line in Filename.readlines():
        line = line.strip('\n')
        line = line.strip(' ')
        line = line.strip('\t')
        Result.append(line)
    print(Result)
    Result = Hong(Result)
    print(Result)
    Result = DeleteNote(Result)
    print(Result)