#!/bin/bash

version=`grep "__version__ = " awl/__init__.py | cut -d "'" -f 2`

git tag "$version"

if [ "$?" != "0" ] ; then
    exit $?
fi

rm -rf build
rm -rf dist
python -m build

twine check dist/*

echo "------------------------"
echo
echo "now do:"
echo "   twine upload dist/*"
echo
