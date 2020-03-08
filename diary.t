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
3.6
    Moring 0.5H
	完成了while的部分，修改了for对于每次变化的量的位置的处理，优化了图形的结构。
	
	Afternoon and Night 3H
	想了半天，终于找到了一种加入If的办法，因为If不会增加循环的层数，但是‘}’仍然会减少层数，所以需要一个标记来避免这种情况
	果然还是出现了问题，因为一开始设计的时候虽然想到了if的特殊性，但是写continue，return和break的时候没有意识到问题的严重性，现在if无法与这三者兼容，正在思考解决方法。
	思来想去，正常情况下，continue和break如果出现，一定是出现在if里，所以决定就此下手改造一下，但这会造成如果在一个循环中直接加入一个break或continue，
	将无法正常产生流程图，但事已至此，鲁棒性难以保持，只能就此牺牲一些了。
    为了防止可能出现的更多问题，先将else的部分完成，然后再修改break和continue

3.7
    Morning 2H
    完成了一点else的更正，即NodeSave的清零工作，现在的if可以嵌套了
	AfterNoon 3H
	完成了printf，scanf，getchar
	出乎我的意料，我的代码一开始设计思路还是比较正确的，虽然加入if之后continue，break与return无法正常工作了，但是通过简单地改写就实现了原来的功能
	但是还是存在一些限制条件，这些限制条件在实际编程中按理不应当出现，因为毫无意义，但是对于代码来说是正确的c语言，可正常运行
3.8
    其实到昨天整个代码已经基本完成了，不过还可以缩减代码长度，多做一些测试，调整流程图美观度，但是晚上又接了学院学生会做快闪视频的工作(｡ŏ_ŏ)，昨天晚上到今天中午在从零探索快闪视频，
	到今天中午已经差不多把视频弄完了。
	
P.S 当前可分析的代码要求：
    1.}请单独一行
	2.保证所有if，for，while都有{}
	3.关于三个退出循环的指令：
	  continue和break只能出现在if中，return只在if或函数最外层，且请不要在这三者后面紧接任何语句，对于代码而言这是没有意义的，而且会出现问题。
	  也不要一个if中的两个分支各有一个，导致这层循环中if之后的代码毫无意义，这样的代码本身毫无意义，而且会出问题。
	4.else不要嵌套else（else中不要再出现else）
	5.输入数组时请按照&a[i]格式输入
	6.printf()现在支持的控制符：%d,%ld,%c,%s,%f,%lf，%u,除此之外请不要在printf中使用%
	