void f()
{
    int *a = calloc(1024, sizeof(a[0]));
}

int main()
{
    int i;

    for (i = 0; i < 1024; i++)
        f();

    return 0;
}


