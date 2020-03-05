3.2
一点思路：
    2H
    其实我并不需要完全实现一个词法分析器，因为我只需要分析出需要构建图形的那些特殊语句，
	然后将内部的语句原封不动的扔进去就行了，所以比如四则运算之类的处理，我都不需要做。
	所以我要做的：
	1.#include的忽略，及宏的替换。
	2.标识符的识别（具体有token 标记；hash 标识符哈希值；name 标识符本身字符串） 
	但是不需要分析标识符的类型，具体的内容，范围之类是什么。
	3.数字暂时只考虑10进制
	4.字符串直接拿过来就可以用，不需要考虑是否转义
	5.注释（包括//和/* */）
	6.算数和逻辑运算符
	7.关键字和内置函数
	8.对于自己手写的函数，可以采用单独使用一张图表表示的方法，在使用的地方引用，因此不需要单独考虑，
	  只需要每一个函数单独建立一个流程图即可（包括主函数）。
3.3
    4H
    现在已经完成了不带参数的宏的展开和注释的消除
	graphviz
	from graphviz import Digraph
	点
	    dot.node('名', '标签')
		dot.node(name='', label='', color='边框颜色')
		grap_g.node("start", label="start",shape="Mdiamond")
		diamond菱形判断
		rectangle矩形大部分
		record圆角开始结束
		parallelogram平行四边形输入输出
		各种形状https://img-blog.csdn.net/2018031722122912?watermark/2/text/Ly9ibG9nLmNzZG4ubmV0L2p1bnJ1aXRpYW4=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70
	线
        dot.edges(['AB',''])
        dot.edge('A','B', '线上的字')
    展示
        dot.view()	
3.4
    2H
    回顾了正则表达式，用正则表达式判断函数，并成功构建了Start和End模块并连接，今天满课，主要时间处理作业，明天课程容量小，继续完成while，for和if的部分。
3.5
    Afernoon 3H
	完成了for和return的部分，有这么几个容易报错的点：
	1.图片view一次之后要关掉。
	2.ParaNode，NodeNum，Floor等更新完了别忘了加减
	3.分清楚是几维的list，以及判断空。
	4.NodeForFloor是返回的位置，NodeForNext【Floor】是每一层的通向结尾的
	
	graphviz可以调整线条出入位置
	tailport,headport='n、ne、e、se、s、sw、w、nw'
	
	Night 3H
	写程序最烦的，就是一开始思路不是非常严谨，中间加加减减，最后思路是弥补了，但是前面的又跟不上了。
	晚上主要完成了Break；修改了最一开始判断函数结束退出的内容；同时让框图更加美观了：for的判断及for内部的安置。
	明天完成while，if，continue。while和for类似，if差别最大，continue还好。