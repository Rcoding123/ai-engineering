---
tags: [python, introducing-python, bytes, bytearray, binary-data]
chapter: 5
---

# Bytes and Bytearray

**What this chapter gives you:** the two types Python uses for raw binary data. `bytes` is
read-only and `bytearray` can be edited in place. You will meet them every time you send an image to
an API, read a streamed response, hash a prompt, or look at what a tokenizer really sees.

## Bytes

A `bytes` object is a fixed row of small integers, each from 0 to 255. Think of beads on a wire:
all the same size, no meaning attached. A `str` is different: it is a row of characters.
Python never mixes the two on its own. You convert on purpose.

> [!info] Key idea: a byte is just a number
> A byte holds one integer in the range 0–255. Python *prints* some bytes as letters (`b"A"`)
> because that is easier to read. The data is still the number 65.

```text
str    :   c     a     f     é          4 characters
           |     |     |     |
encode     v     v     v     v  v        .encode("utf-8")
bytes  :  63    61    66    c3 a9        5 bytes (shown in hex)
           ^                               .decode("utf-8")
```

One character can take more than one byte. That is why `len(text)` and `len(data)` can differ.

### Create with quotes

Put a `b` in front of the quote. Only plain ASCII characters are allowed inside. For any other
value, write two hex digits after a backslash-x.

```python
>>> raw = b"GET\x00\x01\xff"
>>> raw
b'GET\x00\x01\xff'
>>> type(raw)
<class 'bytes'>
>>> len(raw)
6
>>> b"\x41\x42\x43"
b'ABC'
```

### Create with `bytes()`

Give `bytes()` an iterable of integers (a list, a tuple, a `range`), or a single integer.

```python
>>> bytes([72, 105, 33])
b'Hi!'
>>> bytes(3)
b'\x00\x00\x00'
>>> len(bytes(range(256)))
256
>>> bytes([256])
Traceback (most recent call last):
  ...
ValueError: bytes must be in range(0, 256)
```

> [!warning] Trap: `bytes(3)` is not `b"3"`
> A single integer means *length*, not value. `bytes(3)` gives three zero bytes. To get one byte
> whose value is 3, pass a list: `bytes([3])`.

### Create from a hex string

`bytes.fromhex()` reads pairs of hex digits and ignores spaces between the pairs. A lone digit is an
error. It is a *class method*: you call it on `bytes` itself, not on a value ([[11 - Objects|Chapter 11]]).
`.hex()` goes the other way.

```python
>>> bytes.fromhex("48 69 21")
b'Hi!'
>>> bytes.fromhex("4 8")
Traceback (most recent call last):
  ...
ValueError: non-hexadecimal number found in fromhex() arg at position 1
>>> b"Hi!".hex()
'486921'
```

### Encode and decode

Text becomes bytes with `.encode()`. Bytes become text with `.decode()`. You must name the
encoding; use `"utf-8"` unless you have a reason not to. [[17 - Text Data|Chapter 17]] covers the details.

```python
>>> text = "caf\xe9"
>>> data = text.encode("utf-8")
>>> data
b'caf\xc3\xa9'
>>> len(text), len(data)
(4, 5)
>>> data.decode("utf-8") == text
True
>>> data.decode("ascii")
Traceback (most recent call last):
  ...
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 3: ...
```

> [!tip] Rule
> Always pass the encoding by name and decode with the same one you encoded with. Text on the wire (JSON,
> HTTP bodies, files) is almost always UTF-8.

### Index, slice, combine, repeat

Bytes are a sequence, so `[ ]`, slices, `+`, `*`, `in`, and `for` all work.
The catch is what you get back.

> [!example] Type check: indexing vs slicing
> | **Expression** | **Result** | **Type** | **Note** |
> |---|---|---|---|
> | `b[2]` | `97` | `int` | one position gives a *number* |
> | `b[2:3]` | `b"a"` | `bytes` | a slice always gives `bytes` |
> | `b + b` | joined | `bytes` | new object, both sides must be `bytes` |
> | `b * 2` | repeated | `bytes` | new object |
> | `for x in b` | `x` | `int` | the loop walks numbers |
> | `97 in b` | `True` | `bool` | an int tests for one byte |
> | `b"a" in b` | `True` | `bool` | bytes test for a run of bytes |

```python
>>> b = b"\xff\x01abcdef"
>>> b[2]
97
>>> chr(b[2])
'a'
>>> b[2:3]
b'a'
>>> b[-3:]
b'def'
>>> b[0:2] + b"!!"
b'\xff\x01!!'
>>> b"ab" * 2
b'abab'
>>> list(b"Hi")
[72, 105]
>>> b"abc" == "abc"
False
>>> b"abc" + "def"
Traceback (most recent call last):
  ...
TypeError: can't concat str to bytes
```

A useful real-world check is the first few bytes of a file, its "magic number":

```python
>>> data = b"%PDF-1.7 ...rest of file..."
>>> data[:4] == b"%PDF"
True
>>> data.startswith(b"%PDF")
True
```

### Bytes are immutable

You cannot assign to a position. `b1 += b2` looks like an edit, but Python builds a *new* bytes
object and moves the name `b1` onto it. The old one is dropped.

```python
>>> data = bytes([1, 2, 3])
>>> data[0] = 9
Traceback (most recent call last):
  ...
TypeError: 'bytes' object does not support item assignment
>>> before = data
>>> data += bytes([4])
>>> data
b'\x01\x02\x03\x04'
>>> before
b'\x01\x02\x03'
>>> data is before
False
```

## Bytearray

`bytearray` is the editable twin of `bytes`. Every read operation works the same. On top of
that you can change values, change the length, insert, and delete. Use it when you build binary data
piece by piece.

```text
bytes      x = b"ab"          x += b"!"
  before:  x --> [61 62]      x --> [61 62 21]   (a NEW object)
                 [61 62] is dropped

bytearray  x = bytearray(b"ab")     x.extend(b"!")
  before:  x --> [61 62]            x --> [61 62 21]   (the SAME object grew)
```

### Create with `bytearray()`

```python
>>> bytearray()
bytearray(b'')
>>> bytearray([1, 2, 3, 255])
bytearray(b'\x01\x02\x03\xff')
>>> bytearray(4)
bytearray(b'\x00\x00\x00\x00')
>>> bytearray("abc", "ascii")
bytearray(b'abc')
>>> bytearray(b"from bytes")
bytearray(b'from bytes')
```

With a string you must give the encoding as the second argument. `bytearray("abc")` alone is a
`TypeError`.

### Read: index and slice

Same rules as `bytes`, with one difference. A slice of a `bytearray` is a `bytearray`.

```python
>>> ba = bytearray(b"\xff\x01abcdef")
>>> ba[2]
97
>>> ba[4:6]
bytearray(b'cd')
```

### Change one byte or many

```python
>>> ba = bytearray([1, 2, 3, 255])
>>> ba[1] = 127
>>> ba
bytearray(b'\x01\x7f\x03\xff')
>>> ba = bytearray(b"\xff\x01abcdef")
>>> ba[2:5] = b"oops"
>>> ba
bytearray(b'\xff\x01oopsdef')
>>> ba[1] = 300
Traceback (most recent call last):
  ...
ValueError: byte must be in range(0, 256)
```

The slice assignment above replaced three bytes with four, so the array grew. Strings cannot do this.

### `insert()`, `append()`, `extend()`

```python
>>> ba = bytearray(b"abc")
>>> ba.insert(0, 2)
>>> ba.append(4)
>>> ba.extend(b"!!!")
>>> ba
bytearray(b'\x02abc\x04!!!')
>>> ba.append(b"\x04")
Traceback (most recent call last):
  ...
TypeError: 'bytes' object cannot be interpreted as an integer
```

> [!example] Type check: what each method wants
> | **Method** | **Argument** | **Returns** | **Effect** |
> |---|---|---|---|
> | `ba.append(n)` | one `int` 0–255 | `None` | adds one byte at the end |
> | `ba.extend(bs)` | bytes-like or ints | `None` | adds many bytes at the end |
> | `ba.insert(i, n)` | index, `int` | `None` | adds one byte before position `i` |
> | `ba.pop()` | optional index | `int` | removes and returns one byte |
> | `ba.replace(a, b)` | two bytes-like | `bytearray` | a *new* array; `ba` is unchanged |

> [!warning] Trap: `replace()` does not edit in place
> On a `bytearray`, `.replace()` returns a changed *copy*, like `str.replace()`.
> If you ignore the return value, nothing happens.

```python
>>> ba = bytearray(b"\xff\x01abcdef")
>>> new = ba.replace(b"\x01ab", b"XYZ")
>>> new
bytearray(b'\xffXYZcdef')
>>> ba
bytearray(b'\xff\x01abcdef')
```

### Combine, repeat, freeze

```python
>>> bytearray(b"\x01\x02") + bytearray(b"\x03\x04")
bytearray(b'\x01\x02\x03\x04')
>>> bytearray(b"\x01\x02") * 2
bytearray(b'\x01\x02\x01\x02')
>>> frozen = bytes(bytearray(b"hi"))
>>> type(frozen)
<class 'bytes'>
>>> hash(bytearray(b"hi"))
Traceback (most recent call last):
  ...
TypeError: unhashable type: 'bytearray'
```

`bytes(some_bytearray)` makes an immutable copy. Because a `bytearray` can change, it is
unhashable, so it cannot be a dictionary key or a set member ([[09 - Dictionaries and Sets|Chapter 9]]). A `bytes` can.

> [!example] Type check: bytes vs bytearray vs str
> |  | **mutable** | **hashable** | **`x[0]` gives** | **slice gives** |
> |---|---|---|---|---|
> | `bytes` | ✗ | ✓ | `int` | `bytes` |
> | `bytearray` | ✓ | ✗ | `int` | `bytearray` |
> | `str` | ✗ | ✓ | `str` | `str` |

## Where bytes show up in AI work

You will not write much byte-level code, but the types appear at every boundary where data leaves
your program.

| **Situation** | **What you hold** |
|---|---|
| Reading an image or PDF to send to a vision model | `bytes` from `open(path, "rb")` |
| Streaming reply arrives in pieces | `bytes` chunks, collected in a `bytearray` |
| Sending an image as JSON | `base64` turns `bytes` into `bytes` of ASCII, then `.decode()` to `str` |
| Cache key for a prompt | `hashlib` takes `bytes`, so `.encode()` first |
| Byte-level tokenizers | the model sees UTF-8 bytes, so one emoji can be several tokens |

Two short examples, both from the standard library:

```python
>>> import base64, hashlib
>>> base64.b64encode(b"Hi!")
b'SGkh'
>>> base64.b64encode(b"Hi!").decode("ascii")
'SGkh'
>>> hashlib.sha256(b"prompt").hexdigest()[:8]
'cf07194e'
```

Streamed replies can split a multi-byte character across two chunks. Collect the raw bytes first and
decode once at the end:

```python
chunks = [b'{"name": "caf\xc3', b'\xa9", "tokens": 4}']
buf = bytearray()
for chunk in chunks:
    buf.extend(chunk)
print(len(buf), "bytes")
print(buf.decode("utf-8") == '{"name": "caf\xe9", "tokens": 4}')
```

```text
30 bytes
True
```

Decoding each chunk alone would fail, because the two halves of `c3 a9` are in different chunks.

> [!danger] Boss fight: bytes and str look alike but are not
> The same-looking value behaves differently. `b"abc"[0]` is the number 97. `"abc"[0]` is the
> string `"a"`. `b"abc" == "abc"` is `False`, and `+` between them is a
> `TypeError`. 
> **Strategy:** ask "is this data text or raw bytes?" at every boundary. Decode as soon as bytes
> come in and encode as late as possible before they leave. Inside your program, work with `str`.

> [!question]- Practice
> 1. Build a `bytes` value holding the numbers 1 to 5. What does `len()` return?
> 2. What is the difference between `bytes(5)` and `bytes([5])`?
> 3. Given `b = b"hey"`, what are the type and value of `b[0]` and of `b[0:1]`?
> 4. Make a `bytearray` from the numbers 1 to 5, then append 6 and set the first byte to 0.
> 5. Why does `ba.replace(b"a", b"b")` seem to do nothing when you ignore its result?
> 6. A friend encodes a string as UTF-8 and decodes it as ASCII and gets an error. Why?

> [!success] Achievement unlocked: Byte Wrangler
> You can now:
>
> - create `bytes` and `bytearray` from literals, lists, hex strings, and text;
> - predict whether an index or slice returns an `int` or a sequence;
> - convert between `str` and `bytes` with `.encode()` and `.decode()`;
> - pick `bytearray` when data must grow or change, and freeze it with `bytes()`;
> - recognise where bytes appear in API, file, and tokenizer work.

---
Related: [[04 - Strings]] · [[08 - Tuples and Lists]] · [[17 - Text Data]] · [[18 - Binary Data]]
