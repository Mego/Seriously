# Seriously [![Build Status](https://travis-ci.org/Mego/Seriously.svg?branch=v2)](https://travis-ci.org/Mego/Seriously)
A golfing language that is probably terrible. It is currently being developed. Seriously is stack-based, and is unique in its amount of single-character commands. Every character whose ordinal is in [1,255] does something (or will, once I finish development). Character 0 is excluded because it is used as the end-of-file (EOF) character, and so it cannot be used for a command.

All strings are valid programs. There is no such thing as a syntax error, and anything that appears to be a runtime error is actually a no-op (NOP). If you call a command that expects a string on top of the stack, but the top value is an integer, instead of throwing an error, it silently performs a NOP. Eventually, this will not be seen, as the goal for Seriously is for every character and stack state to map to a command.

The name was inspired by [this challenge](http://codegolf.stackexchange.com/questions/58522/seriously-golfscript-cjam-or-pyth).

Try the [online interpreter](http://seriously.tryitonline.net). This is part of [Try it online!](http://tryitonline.net) by @DennisMitchell.

If you are running code locally, you *must* set your terminal text encoding to CP437.

# Commands

See [commands.txt](commands.txt)

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
,p
```

## 99 Bottles of Beer

```
N
```

## Coprimality Test

```
,,g1=
```

## Counting the divisors of a number

```
,w`iXu`Mπ
```
