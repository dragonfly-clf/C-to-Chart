#include<stdio.h>
long long f(int x)
{
	x=x+x;
	return x;
}
int main()
{
	int i,ans,n;
	scanf("%d",&n);
	for (i=1;i<=n;i++)
	{
		ans+=f(i);
	}
	printf("The Answer is %d",ans);
}
