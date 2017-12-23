#!/bin/bash

version=`grep "__version__ = " awl/__init__.py | cut -d "'" -f 2`

git tag "$version"

if [ "$?" != "0" ] ; then
    exit $?
fi

rm -rf build
rm -rf dist
python setup.py sdist
python setup.py bdist_wheel --universal

echo "------------------------"
echo
echo "now do:"
echo "   twine upload dist/*"
echo
