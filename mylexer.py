import re
from graphviz import Digraph

dot = Digraph(comment="The Chart")
Shape = ['Mrecord', 'rectangle', 'diamond', 'parallelogram']#开始，正常，判断，输入输出
NodeName = [str(x) for x in range(1, 100)]
Key = ['int', 'char', 'long long', 'long', 'void', 'unsigned int', 'unsigned long long', 'unsigned long', 'float',
       'double', 'long double']

def CreateNode(Name, Label, Shape):
    dot.node(name=Name, label=Label, shape=Shape)
    return

def CreateEdge(From, To, Label, Head, Tail):
    if Label == 'Yes':
        Tail = 's'
    if Label == 'No':
        Tail = 'e'
    dot.edge(From, To, label=Label, tailport=Tail, headport=Head)
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

def CLean(Para, For):
    Para += For
    Para = Para.replace('{', '').strip(' ').strip(';')
    return Para

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
    ParaNode = ''
    LastIf = []
    FloorOfElse = [[] for i in range(100)]
    FloorOfIf = [[] for i in range(100)]#Floor层If块,因为if不增加循环层的特殊性，需要标记特别处理
    EndOfFor = ['' for i in range(100)]#当前层的for变量改变的信息
    NodeForFloor = []#每一层最后一个，关键性连接语句算作上一层,循环的判断存在这里,类似一个栈，栈顶是当前循环的开端
    NodeToEnd = []#return
    NodeSave = [[] for i in range(100)]#else暂存
    NodeSaveMark = [[] for i in range(100)]#else暂存
    NodeToNext = [[] for i in range(100)]#所有的想要指向Floor层下一个的，意思是被指向的在Floor层，每次要清除
    NodeToNextMark = [[] for i in range(100)]#跟着NodeToNext一起变
    for String in List:
        IsFunc = 0
        if String.find(r'#include') != -1:
            continue

        for key in Key:#判断是不是函数
            x = key + r'\s+' + r'[a-zA-Z\_][0-9a-zA-Z\_]*' + r'[(.)]'
            if re.match(x, String):
                IsFunc = 1
                break

        if IsFunc == 1:#是函数，创造一个新的node
            for key in Key:
                String = String.replace(key, '')
            Floor += 1
            String = 'Start ' + String.replace(' ', '').replace('{', '')
            CreateNode(NodeName[NodeNum], String, Shape[0])
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('')
            NodeNum += 1
            continue

        if String.find('}') != -1:#}为分界

            if FloorOfElse[Floor]:#else结束
                ParaNode = CLean(ParaNode, '')
                if ParaNode != '':  # 建立中间正常块
                    CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                    cnt = 0
                    for NextNode in NodeToNext[Floor]:
                        CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                        cnt += 1
                    while NodeToNext[Floor]:
                        NodeToNextMark[Floor].pop()
                        NodeToNext[Floor].pop()
                    NodeToNext[Floor].append(NodeName[NodeNum])
                    NodeToNextMark[Floor].append('')
                    NodeNum += 1
                    ParaNode = ''

                cnt = 0
                for NextNode in NodeSave[Floor]:#归还
                    NodeToNext[Floor].append(NextNode)
                    NodeToNextMark[Floor].append(NodeSaveMark[Floor][cnt])
                    cnt += 1

                while NodeSave[Floor]:
                    NodeSave[Floor].pop()
                    NodeSaveMark[Floor].pop()

                FloorOfElse[Floor].pop()
                continue

            if FloorOfIf[Floor]:#if的结束
                ParaNode = CLean(ParaNode, '')
                if ParaNode != '':  # 建立中间正常块
                    CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                    cnt = 0
                    for NextNode in NodeToNext[Floor]:
                        CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                        cnt += 1
                    while NodeToNext[Floor]:
                        NodeToNextMark[Floor].pop()
                        NodeToNext[Floor].pop()
                    NodeToNext[Floor].append(NodeName[NodeNum])
                    NodeToNextMark[Floor].append('')
                    NodeNum += 1
                    ParaNode = ''

                NodeToNext[Floor].append(FloorOfIf[Floor][-1])
                NodeToNextMark[Floor].append('No')
                LastIf.append(FloorOfIf[Floor][-1])
                FloorOfIf[Floor].pop()
                continue

            ParaNode = CLean(ParaNode, EndOfFor[Floor])
            if ParaNode != '':#建立中间正常块
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''
                EndOfFor[Floor] = ''

            if NodeForFloor:#结束指向之前的块
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeForFloor[-1], NodeToNextMark[Floor][cnt], 'w', 'w')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeForFloor.pop()

            if Floor == 1:#函数结束
                CreateNode(NodeName[NodeNum], 'End', Shape[0])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNext[Floor].pop()
                    NodeToNextMark[Floor].pop()

                for Node in NodeToEnd:
                    CreateEdge(Node, NodeName[NodeNum], '', 'n', '')
                while NodeToEnd:
                    NodeToEnd.pop()

                NodeNum += 1

            Floor -= 1
            continue

        if re.match(r'\s*break\s*', String):#Break
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            cnt = 0
            for NextNode in NodeToNext[Floor]:
                NodeToNext[Floor-1].append(NextNode)
                NodeToNextMark[Floor-1].append(NodeToNextMark[Floor][cnt])
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNext[Floor].pop()
                NodeToNextMark[Floor].pop()

            continue

        if re.match(r'\s*continue\s*', String):  # Continue
            ParaNode = CLean(ParaNode, EndOfFor[Floor])
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                CreateEdge(NodeName[NodeNum], NodeForFloor[-1], '', 'w', 'w')
                NodeNum += 1
                ParaNode = ''

            continue

        if re.match(r'\s*return[\s;]+', String):#Return
            String = String.replace('return', '').replace(';', '').replace(' ', '')
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':#把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''
                EndOfFor[Floor] = ''

            #创建类似于输出的返回Node
            CreateNode(NodeName[NodeNum], 'Return ' + String, Shape[3])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNextMark[Floor].pop()
                NodeToNext[Floor].pop()
            NodeToEnd.append(NodeName[NodeNum])
            NodeNum += 1
            continue

        if re.match(r'\s*for()', String):#for循环
            String = String.replace('for', '').replace(' ', '').replace('(', '').replace(')', '').replace('{', '')
            x = String.find(';')
            ParaNode += String[0:x+1]
            String = String[x+1:]
            x = String.find(';')
            EndOfFor[Floor+1] = String[x+1:]
            String = String[0:x] + '?'

            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':#把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            CreateNode(NodeName[NodeNum], String, Shape[2])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNextMark[Floor].pop()
                NodeToNext[Floor].pop()
            #yes and no 分支建立
            NodeToNext[Floor+1].append(NodeName[NodeNum])
            NodeToNextMark[Floor+1].append('Yes')
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('No')
            #层栈存入
            NodeForFloor.append(NodeName[NodeNum])

            NodeNum += 1
            Floor += 1
            continue

        if re.match(r'\s*while()', String):  # while循环
            String = String.replace('while', '').replace(' ', '').replace('(', '').replace(')', '').replace('{', '') + '?'
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            CreateNode(NodeName[NodeNum], String, Shape[2])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNextMark[Floor].pop()
                NodeToNext[Floor].pop()
            # yes and no 分支建立
            NodeToNext[Floor + 1].append(NodeName[NodeNum])
            NodeToNextMark[Floor + 1].append('Yes')
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('No')
            # 层栈存入
            NodeForFloor.append(NodeName[NodeNum])

            NodeNum += 1
            Floor += 1
            continue

        if re.match(r'\s*if()', String):#if,Floor不增加
            String = String.replace('if', '').replace(' ', '').replace('(', '').replace(')', '').replace('{', '') + '?'
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            CreateNode(NodeName[NodeNum], String, Shape[2])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNextMark[Floor].pop()
                NodeToNext[Floor].pop()
            # yes and no 分支建立
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('Yes')

            FloorOfIf[Floor].append(NodeName[NodeNum])
            NodeNum += 1
            continue

        if re.match(r'\s*else', String):#遇到else，需要防止上一个if中的东西连过来,NodeToNext备份
            FloorOfElse[Floor].append(LastIf[-1])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                if NextNode != LastIf[-1]:
                    NodeSave[Floor].append(NextNode)
                    NodeSaveMark[Floor].append(NodeToNextMark[Floor][cnt])
                cnt += 1

            while NodeToNext[Floor]:
                NodeToNext[Floor].pop()
                NodeToNextMark[Floor].pop()

            NodeToNext[Floor].append(LastIf[-1])
            NodeToNextMark[Floor].append('No')
            LastIf.pop()
            continue

        if String.find('getchar()') != -1:#getchar
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            String = "Input " + String.replace('getchar()', '').replace(' ', '').replace('=', '').strip(';')
            CreateNode(NodeName[NodeNum], String, Shape[3])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNext[Floor].pop()
                NodeToNextMark[Floor].pop()
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('')
            NodeNum += 1
            continue

        if String.find('scanf') != -1:
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            x = String.find('"')
            String = String[x+1:]
            x = String.find('"')
            String = String[x+2:]
            String = "Input " + String.replace('&', '').replace(')', '').strip(';')

            CreateNode(NodeName[NodeNum], String, Shape[3])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNext[Floor].pop()
                NodeToNextMark[Floor].pop()
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('')
            NodeNum += 1
            continue

        if String.find('printf') != -1:
            ParaNode = CLean(ParaNode, '')
            if ParaNode != '':  # 把之前的连续普通先连上
                CreateNode(NodeName[NodeNum], ParaNode, Shape[1])
                cnt = 0
                for NextNode in NodeToNext[Floor]:
                    CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                    cnt += 1
                while NodeToNext[Floor]:
                    NodeToNextMark[Floor].pop()
                    NodeToNext[Floor].pop()
                NodeToNext[Floor].append(NodeName[NodeNum])
                NodeToNextMark[Floor].append('')
                NodeNum += 1
                ParaNode = ''

            x = String.find('"')
            String = String[x+1:]
            x = String.find('"')
            Str = String[x+2:]
            String = String[:x]
            vName = Str.split(',')
            cnt = 0

            while String.find('%') != -1:
                x = String.find('%')
                Leng = 1
                if (String[x+1] == 'l'):
                    Leng = 2
                String = String[:x] + vName[cnt] + String[x+Leng+1:]
                cnt += 1

            String = "Output " + String.replace(')', '').strip(';')

            CreateNode(NodeName[NodeNum], String, Shape[3])
            cnt = 0
            for NextNode in NodeToNext[Floor]:
                CreateEdge(NextNode, NodeName[NodeNum], NodeToNextMark[Floor][cnt], 'n', '')
                cnt += 1
            while NodeToNext[Floor]:
                NodeToNext[Floor].pop()
                NodeToNextMark[Floor].pop()
            NodeToNext[Floor].append(NodeName[NodeNum])
            NodeToNextMark[Floor].append('')
            NodeNum += 1
            continue

        ParaNode = ParaNode + String


if __name__ == '__main__':#默认所有的分层都有{}，所有}都是单独一行
    Result = []
    filename = input("Please input the path:")
    Filename = open(filename)
    for line in Filename.readlines():
        line = line.strip('\n')
        line = line.strip(' ')
        line = line.strip('\t')
        Result.append(line)
    Result = Hong(Result)
    Result = DeleteNote(Result)
    BuildChart(Result)
    dot.view()