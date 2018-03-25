# Actually [![Build Status](https://travis-ci.org/Mego/Seriously.svg?branch=master)](https://travis-ci.org/Mego/Seriously) [![Build status](https://ci.appveyor.com/api/projects/status/v2w8ek1dypxb36s9?svg=true)](https://ci.appveyor.com/project/Mego/seriously) [![PyPI](https://img.shields.io/pypi/v/seriously.svg?maxAge=2592000?style=plastic)](https://pypi.python.org/pypi/seriously) [![license](https://img.shields.io/github/license/Mego/Seriously.svg?maxAge=2592000?style=plastic)](LICENSE) [![codecov](https://codecov.io/gh/Mego/Seriously/branch/master/graph/badge.svg)](https://codecov.io/gh/Mego/Seriously) [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/1173/badge)](https://bestpractices.coreinfrastructure.org/projects/1173)
A golfing language that is probably terrible. It is currently being developed. Actually is the spiritual successor to Seriously. Actually is stack-based, and is unique in its amount of single-character commands. Every character whose ordinal is in [0,255] does something (or will, once I finish development).

All strings are valid programs. There is no such thing as a syntax error, and anything that appears to be a runtime error is actually a no-op (NOP). If you call a command that expects a string on top of the stack, but the top value is an integer, instead of throwing an error, it silently performs a NOP. Eventually, this will not be seen, as the goal for Seriously is for every character and stack state to map to a command.

Seriously's name was inspired by [this challenge](http://codegolf.stackexchange.com/questions/58522/seriously-golfscript-cjam-or-pyth). Actually followed because it is also an adverb, and it also looks funny in answer headers.

Try the [online interpreter](http://actually.tryitonline.net). This is part of [Try it online!](http://tryitonline.net) by @DennisMitchell.

# Commands

See [commands.txt](docs/commands.txt)

# Examples

## Hello, World!

```
H
```

If you prefer a more interesting version:

```
"Hello, World!"
```

## Primality Test

```
p
```

## 99 Bottles of Beer

```
N
```

## Coprimality Test

```
g1=
```

## Counting the divisors of a number

```
w⌠iXu⌡Mπ
```

or

```
÷l
```
