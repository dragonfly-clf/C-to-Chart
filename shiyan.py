from graphviz import Digraph

dot = Digraph(comment="The Chart")
Shape = ['diamond', 'rectangle', 'record', 'parallelogram']
NodeName = [str(x) for x in range(1, 100)]

def CreateNode(Name, Label, Shape):
    dot.node(name=Name, label=Label, shape=Shape)

def CreateEdge(From, To, Label):
    dot.edge(From, To, Label)

if __name__=="__main__":
    cnt = 0
    CreateNode(NodeName[cnt], 'Start', Shape[0])
    cnt += 1
    CreateNode(NodeName[cnt], 'END', Shape[3])
    CreateEdge(NodeName[0], NodeName[1], 'have a try')
    dot.view()