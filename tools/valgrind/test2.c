void *f()
{
	int *a = calloc(16, sizeof(a[0]));
	free(a);
	return a;
}

int main()
{
	int *a = f();
	free(a);
	return 0;
}


