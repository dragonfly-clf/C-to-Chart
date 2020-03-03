from graphviz import Digraph
b = ['A', 'B', 'C', 'D']
a = ['start', 'a=b+c', '(Output) a', 'end']
dot = Digraph(comment="The Test One")
dot.node(name=b[0], label=a[0], shape='record')
dot.node(name=b[1], label=a[1], shape='rectangle')
dot.node(name=b[2], label=a[2], shape='parallelogram')
dot.node(name=b[3], label=a[3], shape='record')
for i in range(0,3):
    dot.edge(b[i], b[i+1])

dot.view()

