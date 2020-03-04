import re
from graphviz import Digraph

dot = Digraph(comment="The Chart")
Shape = ['record', 'rectangle', 'diamond', 'parallelogram']#开始，正常，判断，输入输出
NodeName = [str(x) for x in range(1, 100)]
Key = ['int', 'char', 'long long', 'long', 'void', 'unsigned int', 'unsigned long long', 'unsigned long', 'float', 'double', 'long double']

def CreateNode(Name, Label, Shape):
    dot.node(name=Name, label=Label, shape=Shape)
    return

def CreateEdge(From, To, Label):
    dot.edge(From, To, Label)
    return

def Hong(List):#Define
    AnsList = []
    Anslist = []
    Old = []
    New = []
    sum = 0

    for String in List:
        hong = String.find('#define')
        if hong == -1:
            AnsList.append(String)
            continue
        String = String[hong+8:].strip(' ')
        Space = String.find(' ')
        Old.append(String[:Space])
        New.append(String[Space+1:])
        sum += 1

    for String in AnsList:
        cnt = 0
        for Sa in Old:
            if sum > cnt:
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

            if Mark == 1:
                String = String[0: LeftNumber-1] + String[LeftNumber:]
                LeftNumber -= 1
                if Left == 3 and word == '/':
                    Mark = 0
                    Left = 0
                if word == '*':
                    Left = 3
                continue

            if Left == 0 and word == '/':
                Left = 1
                continue

            if word == '/' and Left == 1:#说明是单边的注释
                String = String[0: LeftNumber-2]
                Left = 0
                break

            if word == '*' and Left == 1:#说明是双边注释的前半边
                Mark = 1
                Left = 2
                String = String[0: LeftNumber-2] + String[LeftNumber:]
                LeftNumber -= 2
                continue

            if Left == 1 and word != '/':#错认了
                Left = 0
                continue

        AnsList.append(String)
    return AnsList

def BuildChart(List):
    NodeNum = 0#每次新建Node要+1
    Floor = 0#每次进入不同层要加减
    NodeForFloor = []#每一层最后一个，关键性连接语句算作上一层，比如函数Start算作0层
    NodeToNext = []#每次要清除
    NodeToNextMark = []#跟着NodeToNext一起变
    for String in List:
        IsFunc = 0

        for key in Key:
            x = key + r'\s+' + r'[a-zA-Z\_][0-9a-zA-Z\_]*' + r'[(.)]'
            if re.match(x, String):#判断是不是函数
                IsFunc = 1
                break
        if IsFunc == 1:#是函数，创造一个新的node
            for key in Key:
                String = String.replace(key, '')
            String = 'Start ' + String.replace(' ', '').replace('{', '')
            CreateNode(NodeName[NodeNum], String, Shape[0])
            NodeForFloor.append(NodeName[NodeNum])
            NodeToNext.append(NodeName[NodeNum])
            NodeToNextMark.append('')
            NodeNum += 1
            Floor += 1
            continue

        if String.find('}') != -1:
            Floor -= 1
            NodeForFloor.pop()
            if Floor == 0:#函数结束
                CreateNode(NodeName[NodeNum], 'End', Shape[0])
                cnt = 0
                for NextNode in NodeToNext:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[cnt])
                    cnt += 1
                while NodeToNext:
                    NodeToNext.pop()
                    NodeToNextMark.pop()
                NodeNum += 1
                continue



    return

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
    BuildChart(Result)
    dot.view()