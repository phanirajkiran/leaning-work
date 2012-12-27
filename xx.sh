
#!/bin/bash -x
KERNEL=bzImage
xx()
{
	PARA=${@:-$KERNEL}
	echo $PARA
}
xx "$@"
