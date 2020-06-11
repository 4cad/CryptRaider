# CryptRaider
Some utilities for crypto CTF challenges

# Test
Run tests using the `python3 -m unittest` command.

I generally run the tests on windows using the windows subsystem for linux. Package gmpy2 is required.

Also, to package and publish run the following:

```
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```