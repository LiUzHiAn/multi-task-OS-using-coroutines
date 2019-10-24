# Overview

This OS is from the course material of `A Curious Course on Coroutines and Concurrency`, which was designed by David Beazley.

Copyright (C) 2009, All Rights Reserved David Beazley [http://www.dabeaz.com](http://www.dabeaz.com)


# multi-task OS intro

This is a mini multi-task Operating System using coroutines in Python 3. In this OS, we simulate the job of OS to fulfill this features:

- Tasks can run concurrently
- Tasks can create, destroy, and wait for tasks
- Tasks can perform I/O operations
- You can even write a concurrent server

# prerequisite
Python 3.6
No third party

# What I did
Based on the original code of David, I reproduce this and transplant it to python 3. It turns out that things are almost the same except the `print()` statement.
I did a tiny improvement of this OS, specifically, I add an syscall named `DestroyConn()` to remove the task as soon as possible, right after the connection between client and server was shutdown.
In this way, we can aviod the next CPU executing in vain. (Why to do a thing we know that couldn't happen?)

I changed the construction of the files for better checking out.


# Usage
```
$ python echo_server.py
$ python client.py
[$ python client.py]
[$ python client.py]

```
You can run the client so many times as you want. The non-blocking I/O is supported.
