
#!/bin/bash -x
tmpdir=/tmp
defvalue=1

DIR=${@:-$tmpdir}   # Defaults to /tmp dir.
VALUE=${2:-$defvalue}           # Default value is 1.

echo $DIR
