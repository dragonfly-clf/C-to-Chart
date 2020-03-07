1.}没有单独一行
   if (a<b){
   b++;}
2.缺少{}（即使是合法的也请给一个{}，秋梨膏）
   for (i=1;i<=n;i++) p++;
3.continue,break,return
  (1) for(i=1;i<=n;i++)
      {
          ans+=1;
		  break;#for里面直接写个这个还写for干啥
      }
  (2) while ()
      {
	      if (ans>b)
		  {
		      break;
			  haha;#^_^哈哈，即使这一句运行不了我也要写上
		  }
	  }
4.else不要嵌套else（这个是我的程序else写的问题）
  if (1>2)
  {
  }
  else
  {
      if(2>1)
	  {
	  }
	  else
	  {
	  }
  }
5.数组按照&a[i]格式，不要用a
  scanf("%d",a)
6.printf控制符之外的%
  printf("%%%zcytql")
  