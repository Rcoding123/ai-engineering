---
tags: [python, introducing-python, lists, tuples, sequences]
chapter: 8
---

# Tuples and Lists

**What this chapter gives you:** the two ordered containers you will use all day. A `tuple` is a
fixed row of items. A `list` is a row you can grow, shrink, and reorder. You will learn to slice them,
sort them, copy them without surprises, and build new ones with comprehensions. A prompt history, a batch of
documents, and a list of embeddings are all lists.

> [!info] Key idea: sequences, mutable and immutable
> A *sequence* holds items in order and is read by position (index). Strings and bytes are
> sequences of one kind of item. Tuples and lists can hold *any* mix of types, even other lists.
>
>
> | **Type** | **mutable?** | **hashable?** | **Literal** |
> |---|---|---|---|
> | `str`, `bytes` | ✗ | ✓ | `"ab"`, `b"ab"` |
> | `tuple` | ✗ | ✓ (if every item is) | `(1, 2)` |
> | `list` | ✓ | ✗ | `[1, 2]` |
> | `bytearray` | ✓ | ✗ | `bytearray(b"ab")` |

## Tuples

### Create with commas and ()

The comma makes the tuple, not the parentheses. Parentheses only make it easier to see. The one place where
the comma really matters is a tuple with one item.

```python
>>> empty = ()
>>> pair = 1024, "tokens"
>>> pair
(1024, 'tokens')
>>> one = ("haiku",)
>>> one, type(one)
(('haiku',), <class 'tuple'>)
>>> not_a_tuple = ("haiku")
>>> type(not_a_tuple)
<class 'str'>
```

> [!warning] Trap: the one-item tuple
> `("haiku")` is just a string in brackets. You need the trailing comma: `("haiku",)`. This also
> bites when you pass a one-item tuple to a function: `f(("a",))`, because `f("a",)` is just the
> string.

### Unpacking and swapping

Assigning a tuple to several names takes it apart. The count must match, unless you use `*name` to
soak up the extras (it always becomes a list).

```python
>>> usage = (812, 143)
>>> tokens_in, tokens_out = usage
>>> tokens_in, tokens_out
(812, 143)
>>> a, b, c = usage
Traceback (most recent call last):
  ...
ValueError: not enough values to unpack (expected 3, got 2)
>>> first, *rest = [10, 20, 30, 40]
>>> first, rest
(10, [20, 30, 40])
>>> x, y = 1, 2
>>> x, y = y, x
>>> x, y
(2, 1)
```

The swap works because the right side is built into a tuple first, then unpacked. No temporary variable is
needed.

### Convert with tuple()

`tuple(iterable)` builds a tuple from anything you can loop over.

```python
>>> tuple(["a", "b"]), tuple("ab"), tuple(b"\x01\x02")
(('a', 'b'), ('a', 'b'), (1, 2))
```

### What you can do with a tuple

Read it, slice it, combine it, repeat it, compare it, loop over it. You cannot change it.

```python
>>> t = (1, 2, 3)
>>> t[0], t[-1], t[1:]
(1, 3, (2, 3))
>>> t[0] = 9
Traceback (most recent call last):
  ...
TypeError: 'tuple' object does not support item assignment
>>> t + (4,), t * 2
((1, 2, 3, 4), (1, 2, 3, 1, 2, 3))
>>> (7, 2) < (7, 2, 9), (7, 2) == (7, 2, 9)
(True, False)
>>> for word in ("fresh", "out"):
...     print(word)
fresh
out
```

"Modify" with `+=` only *looks* like a change. Python builds a new tuple and moves the name onto
it, exactly as for `bytes`.

```python
>>> t1 = ("Fee", "Fie")
>>> before = t1
>>> t1 += ("Foe",)
>>> t1, before, t1 is before
(('Fee', 'Fie', 'Foe'), ('Fee', 'Fie'), False)
```

> [!warning] Trap: immutable does not mean "deeply frozen"
> A tuple cannot re-point its slots, but if a slot holds a *list*, that list can still change. The
> tuple is then not hashable.

```python
>>> record = ("log", [1, 2])
>>> record[1].append(3)
>>> record
('log', [1, 2, 3])
>>> hash(record)
Traceback (most recent call last):
  ...
TypeError: unhashable type: 'list'
```

A *named tuple* lets you read items by name as well as by position. It is covered in [[11 - Objects|Chapter 11]].

## Lists

A list keeps items in order, allows duplicates, and can be changed in place. Use one whenever the contents
or the length can change.

### Create with [], list(), and split()

```python
>>> empty = []
>>> mixed = [1, "two", [3, 4], None]
>>> list("cat"), list((1, 2)), list(range(3))
(['c', 'a', 't'], [1, 2], [0, 1, 2])
>>> "9/19/2024".split("/")
['9', '19', '2024']
>>> "a/b//c".split("/")
['a', 'b', '', 'c']
>>> "a/b//c".split("//")
['a/b', 'c']
>>> "one  two   three".split()
['one', 'two', 'three']
```

Two repeated separators give an empty string between them. `split()` with no argument splits on any run
of whitespace and drops the empties.

### Index and slice

An index counts from 0 at the left, or from -1 at the right. A slice `seq[start:stop:step]` returns a
*new list* of the same type. The easiest way to read a slice is to imagine the numbers sitting on the
*lines between* items: the slice runs from the start line to the stop line, so the stop item is not
included.

```text
 item index:    0     1     2     3     4
             +-----+-----+-----+-----+-----+
  row =      |  p  |  q  |  r  |  s  |  t  |
             +-----+-----+-----+-----+-----+
 negative:    -5    -4    -3    -2    -1
 slice lines: 0     1     2     3     4     5
                    [-------------)           row[1:4] -> [q, r, s]
```

```python
>>> row = ["p", "q", "r", "s", "t"]
>>> row[0], row[-1]
('p', 't')
>>> row[1:4], row[:2], row[-2:]
(['q', 'r', 's'], ['p', 'q'], ['s', 't'])
>>> row[::2], row[::-1]
(['p', 'r', 't'], ['t', 's', 'r', 'q', 'p'])
>>> row[10:], row[-9:2]
([], ['p', 'q'])
>>> row[5]
Traceback (most recent call last):
  ...
IndexError: list index out of range
```

> [!example] Type check: index vs slice
> `row[2]` returns *one item* (any type; here a `str`) and raises `IndexError` when out of
> range. `row[2:3]` returns a *list* (here with one item) and never raises: out-of-range ends
> quietly snap to the edge. A slice is a copy, so assigning to it does not change `row`.

### Add items

```python
>>> q = ["a", "b", "c"]
>>> q.append("d")
>>> q.insert(0, "z")
>>> q.extend(["x", "y"])
>>> q
['z', 'a', 'b', 'c', 'd', 'x', 'y']
>>> q.append(["m", "n"])
>>> q[-1]
['m', 'n']
>>> q += ["end"]
>>> print(q.append("e"))
None
```

> [!warning] Trap: append vs extend
> `append(x)` adds *one item*, even if `x` is a list. `extend(it)` (and `+=`)
> adds each item of `it`. Using `append` with a list gives a list inside the list.

> [!warning] Trap: methods that change a list return None
> `append`, `extend`, `insert`, `sort`, `reverse`, `remove`, and `clear`
> change the list in place and return `None`. Writing `names = names.sort()` replaces your list with
> `None`.

### Change items

Assigning to an index replaces one item. Assigning to a slice replaces a whole stretch, and the new stretch
can be any iterable of any length.

```python
>>> n = [1, 2, 3, 4]
>>> n[0] = "one"
>>> n[1:3] = [7, 8, 9]
>>> n
['one', 7, 8, 9, 4]
>>> n[1:3] = []
>>> n
['one', 9, 4]
>>> n[10] = 1
Traceback (most recent call last):
  ...
IndexError: list assignment index out of range
```

### Remove items

| **Want to** | **Use** | **Returns** | **If missing** |
|---|---|---|---|
| delete by position | `del m[i]` | (statement) | `IndexError` |
| delete by value | `m.remove(v)` | `None` | `ValueError`; removes the first match only |
| take out by position | `m.pop(i)` | the item | `IndexError`; default `i` is `-1` |
| empty the list | `m.clear()` | `None` | – |

```python
>>> m = ["a", "b", "c", "b"]
>>> del m[0]
>>> m.remove("b")
>>> m
['c', 'b']
>>> m.pop(), m.pop(0)
('b', 'c')
>>> m.pop()
Traceback (most recent call last):
  ...
IndexError: pop from empty list
>>> ["a"].remove("z")
Traceback (most recent call last):
  ...
ValueError: list.remove(x): x not in list
```

`append()` with `pop()` gives a stack (last in, first out). `append()` with `pop(0)` gives
a queue (first in, first out), but `pop(0)` is slow on big lists. For queues, use
`collections.deque` ([[12 - Modules and Packages|Chapter 12]]).

### Find and count

```python
>>> w = ["a", "b", "a"]
>>> w.index("a"), w.count("a"), "b" in w, len(w)
(0, 2, True, 3)
>>> w.index("z")
Traceback (most recent call last):
  ...
ValueError: 'z' is not in list
>>> nums = [3, 9, 4]
>>> min(nums), max(nums), sum(nums)
(3, 9, 16)
```

`index()` returns the *first* position and raises `ValueError` if the value is absent, so check
with `in` first when it may be missing. If you test membership a lot, a set is faster ([[09 - Dictionaries and Sets|Chapter 9]]).

### join() is the opposite of split()

`join()` is a *string* method. The separator is the string you call it on, and the list is the
argument. It returns a `str` and needs every item to already be a string.

```python
>>> parts = ["Harry", "Hermione", "Ron"]
>>> ", ".join(parts)
'Harry, Hermione, Ron'
>>> ", ".join(parts).split(", ") == parts
True
>>> ", ".join([1, 2])
Traceback (most recent call last):
  ...
TypeError: sequence item 0: expected str instance, int found
>>> ", ".join([str(n) for n in [1, 2]])
'1, 2'
```

### Sort with sort() or sorted()

|  | **Changes the list?** | **Returns** | **Works on** |
|---|---|---|---|
| `m.sort()` | yes, in place | `None` | lists only |
| `sorted(x)` | no | a new `list` | any iterable |
| `m.reverse()` | yes, in place | `None` | lists only |
| `reversed(x)` | no | an iterator | any sequence |

```python
>>> scores = [0.9, 0.2, 0.5]
>>> sorted(scores)
[0.2, 0.5, 0.9]
>>> scores
[0.9, 0.2, 0.5]
>>> result = scores.sort(reverse=True)
>>> result is None, scores
(True, [0.9, 0.5, 0.2])
>>> sorted([1, "a"])
Traceback (most recent call last):
  ...
TypeError: '<' not supported between instances of 'str' and 'int'
```

The `key=` argument names a function that turns each item into the value to compare. The items
themselves are not changed.

```python
>>> words = ["Banana", "apple", "cherry"]
>>> sorted(words)
['Banana', 'apple', 'cherry']
>>> sorted(words, key=str.lower)
['apple', 'Banana', 'cherry']
>>> runs = [("haiku", 0.4), ("opus", 3.1), ("sonnet", 1.2)]
>>> sorted(runs, key=lambda r: r[1], reverse=True)
[('opus', 3.1), ('sonnet', 1.2), ('haiku', 0.4)]
```

(`lambda r: r[1]` is a tiny unnamed function, which [[10 - Functions|Chapter 10]] explains. It means "given `r`,
give back `r[1]`".) Plain uppercase letters sort before lowercase, and a sort that is
*stable* keeps the original order of ties.

### Assignment makes a second name, not a second list

A variable is a label. `b = a` sticks a second label on the *same* list, so a change through one
name shows through the other. To get an independent list, copy it with `a.copy()`, `list(a)`, or
`a[:]`.

```text
  b = a                              b = a.copy()

  a ----\                            a ---> [1, 2, 3]
         +--> [1, 2, 3]
  b ----/                            b ---> [1, 2, 3]     (a second list)

  b is a  -> True                    b is a  -> False
  a[0] = 9  also changes b           a[0] = 9  leaves b alone
```

```python
>>> a = [1, 2, 3]
>>> b = a
>>> a[0] = "changed"
>>> b
['changed', 2, 3]
>>> b is a
True
>>> c, d, e = a.copy(), list(a), a[:]
>>> a[1] = "x"
>>> c, d == c, e is a
(['changed', 2, 3], True, False)
```

### Copy everything with deepcopy()

`copy()`, `list()`, and `[:]` are *shallow*: they copy the outer list but reuse the inner
objects. If an item is itself a list, both outer lists point at the *same* inner list. For a fully
independent copy, use `copy.deepcopy()` from the standard library.

```text
  a = [1, 2, X] ----.
  b = a.copy()       +--> X = [8, 10]    (shared inner list, shallow)
        [1, 2, X] --'

  c = deepcopy(a)  [1, 2, Y] ---> Y = [8, 9]   (its own inner list)
```

```python
>>> import copy
>>> a = [1, 2, [8, 9]]
>>> b = a.copy()
>>> c = copy.deepcopy(a)
>>> a[2][1] = 10
>>> b, c
([1, 2, [8, 10]], [1, 2, [8, 9]])
>>> b[2] is a[2], c[2] is a[2]
(True, False)
```

> [!danger] Boss fight: two names, one list (and shared insides)
> Almost every strange "my data changed by itself" bug is aliasing. `b = a` shares the list. Even
> `a.copy()` shares any *inner* lists, dicts, or sets. This applies to *every* mutable type. 
> **Strategy:** ask "is this one object or two?" with `is`. Copy when you need independence. Use
> `deepcopy` when the data is nested. Prefer building new lists over editing a shared one.

> [!warning] Trap: multiplying a list of lists repeats one inner list
> Multiplying a list repeats *references*, so `[[0] * 3] * 2` holds the same inner list twice. The rows of the grid below are one list shown twice. Build
> each row separately with a comprehension.

```python
>>> grid = [[0] * 3] * 2
>>> grid[0][0] = 1
>>> grid
[[1, 0, 0], [1, 0, 0]]
>>> grid = [[0] * 3 for _ in range(2)]
>>> grid[0][0] = 1
>>> grid
[[1, 0, 0], [0, 0, 0]]
```

### Compare and iterate

Lists are compared item by item from the left, like words in a dictionary. A shorter list that matches
the start is smaller. Iteration is `for item in list`; `break`, `continue`, and `else`
work as in [[07 - For and While|Chapter 7]].

```python
>>> [7, 2] == [7, 2, 9], [7, 2] < [7, 2, 9], [3] < [2, 9]
(False, True, False)
>>> for cheese in ["brie", "gjetost", "havarti"]:
...     if cheese.startswith("g"):
...         print("skip", cheese)
...         break
...     print(cheese)
... else:
...     print("no g found")
brie
skip gjetost
```

### Iterate several sequences with zip()

`zip(a, b, ...)` pairs up items at the same position and stops at the shortest input. It returns a
lazy iterator of tuples, so wrap it in `list()` to see them, and you can unpack each tuple in the
`for` line.

```text
  models  :  haiku     sonnet    opus
  prices  :  0.1       0.3       1.0
             |         |         |
  zip ->  (haiku,0.1) (sonnet,0.3) (opus,1.0)     one tuple per position
```

```python
>>> models = ["haiku", "sonnet", "opus"]
>>> prices = [0.1, 0.3, 1.0]
>>> for name, price in zip(models, prices):
...     print(name, price)
haiku 0.1
sonnet 0.3
opus 1.0
>>> dict(zip(models, prices))
{'haiku': 0.1, 'sonnet': 0.3, 'opus': 1.0}
>>> list(zip("ab", [1, 2, 3]))
[('a', 1), ('b', 2)]
```

If the lengths differ, `zip()` silently drops the extras. Two ways to stay in control:

```python
>>> from itertools import zip_longest
>>> list(zip_longest([1, 2], ["a", "b", "c"], fillvalue=0))
[(1, 'a'), (2, 'b'), (0, 'c')]
>>> list(zip([1], [1, 2], strict=True))
Traceback (most recent call last):
  ...
ValueError: zip() argument 2 is longer than argument 1
```

### List comprehensions

A comprehension builds a list in one expression: `[expression for item in iterable if condition]`.
The `if` part is optional. It reads as: for each item, if the condition is true, put the expression's
value in the new list. The loop moves inside the brackets.

```text
  [  n * 2        for n in range(10)       if n % 2 == 0   ]
     ^ (3)           ^ (1)                    ^ (2)
     value to add    take each item           keep only if True
```

```python
>>> [n * 2 for n in range(4)]
[0, 2, 4, 6]
>>> [n for n in range(10) if n % 3 == 0]
[0, 3, 6, 9]
>>> words = ["a", "bb", "ccc"]
>>> [len(w) for w in words]
[1, 2, 3]
>>> [(r, c) for r in range(2) for c in range(2)]
[(0, 0), (0, 1), (1, 0), (1, 1)]
```

With two `for` clauses, the first is the outer loop. The comprehension above equals a nested loop that
appends `(r, c)` at the bottom.

> [!warning] Trap: an `if` at the end filters; an `if/else` at the front transforms
> These look alike but do different jobs. A trailing `if` (no `else`) *drops* items. A
> conditional expression in the value slot keeps every item and picks a value for each. Remember the order
> from [[06 - If and Match|Chapter 6]]: value, `if` test, `else` value.

```python
>>> words = ["a", "bb", "ccc"]
>>> [w for w in words if len(w) > 1]
['bb', 'ccc']
>>> ["long" if len(w) > 1 else "short" for w in words]
['short', 'long', 'long']
```

### Lists of lists

A list can hold lists. Use one index per level, left to right: the first picks the inner list, the next
picks inside it.

```python
>>> batches = [["a", "b"], ["c"], []]
>>> batches[0], batches[0][1]
(['a', 'b'], 'b')
>>> len(batches), [len(b) for b in batches]
(3, [2, 1, 0])
>>> [item for batch in batches for item in batch]
['a', 'b', 'c']
```

The last line *flattens* one level. The outer `for` comes first, just as in nested loops.

## Tuples versus lists

You can often use either. The choice is about what you mean.

|  | **tuple** | **list** |
|---|---|---|
| Mutable? | no | yes |
| Methods | only `count` and `index` | many (`append`, `sort`, ...) |
| Can be a dict key? | yes, if all items are hashable | no |
| Typically holds | a fixed record of *different* things: `(model, price)` | many *similar* items: a list of prices |
| Size | a little smaller | over-allocates room to grow |
| Safe from accidents? | yes, nobody can edit it by mistake | no |

> [!tip] Rule
> Use a tuple for a small fixed record or a function's multiple results. Use a list for a collection that
> grows, shrinks, or gets sorted. In everyday code you will use lists (and dicts, [[09 - Dictionaries and Sets|Chapter 9]]) far more.

## There are no tuple comprehensions

Lists, dicts, and sets have comprehensions. Tuples, strings, and bytes do not. Swapping the square brackets
for parentheses does *not* give a tuple. It gives a *generator expression*: a lazy iterator that
produces items one at a time and can be read only once. Wrap it in `tuple()` to get a tuple.

```python
>>> g = (n * n for n in range(3))
>>> type(g)
<class 'generator'>
>>> tuple(g)
(0, 1, 4)
>>> tuple(g)
()
>>> sum(n * n for n in range(4))
14
```

Because a generator makes values only when asked, it is the right tool for big or endless data, for example
processing a million documents without holding them all in memory. [[10 - Functions|Chapter 10]] covers generators fully.

> [!question]- Practice
> 1. Make a list `prices = [0.1, 0.3, 1.0, 0.6]`. Write the slices that give the first two, the last two, and the list reversed. What is each result's type?
> 2. What do `x = [3, 1, 2].sort()` and `y = sorted([3, 1, 2])` leave in `x` and `y`?
> 3. After `a = [1, [2, 3]]; b = a.copy(); b[1].append(4)`, what is `a`? Why? What one change makes `a` stay untouched?
> 4. Write a list comprehension that gives the lengths of only the words longer than 3 letters in a list of words.
> 5. What is the difference between `append` and `extend`? Show each with `[1, 2]` and `[3, 4]`.
> 6. Why does `("hello")` not make a tuple, and what makes the one-item tuple?

> [!success] Achievement unlocked: List Keeper
> You can now:
>
> - build tuples and lists, unpack them, and slice with start, stop, and step;
> - add, change, find, and remove items, knowing which methods return `None`;
> - sort with `sort`, `sorted`, and `key=`, and pair sequences with `zip`;
> - tell aliasing, shallow copy, and deep copy apart and pick the right one;
> - write list comprehensions with filters and conditional values.

---
Related: [[04 - Strings]] · [[05 - Bytes and Bytearray]] · [[07 - For and While]] · [[09 - Dictionaries and Sets]] · [[10 - Functions]] · [[11 - Objects]]
