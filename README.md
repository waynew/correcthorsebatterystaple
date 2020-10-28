correcthorsebatterystaple
=========================

this: http://xkcd.com/936/

You can try it out at https://correcthorsebatterystaple.waynewerner.com

I don't log which passwords I generate, but if you're paranoid about security
you probably should just generate the passwords locally.

---

This project started off using Flask. Then I realized that was overkill. I
decdied to make this server be able to run with pure Python, because there's
literally no reason *not* to.

The easiest way to try it out for yourself:

    python3 -m pip install --user chbs

Then you can run:

    chbs -h

And that should tell you everything you need to know.

Or, clone this repo and run:

    python3 chbs/server.py

And then connect to it:

    $ curl localhost:8000
    correct horse battery staple$

Yeah. It won't return an ending newline. That's intentional.

---

I also decided that for funsies I should make this into a test. What is the difference between just:

- Single threaded server.
- A server using `select`.
- A server using `epoll`.
- A multithreaded server.
- A server using asyncio.
- A server using an aiohttp server.

My theory is that a single threaded server should be about as good as it gets.
Or possibly using epoll or select? Given the size of the data that we're
returning, I don't think that I'll get a lot of difference between any of these
servers. We shall see.

The first server that I will produce will be just a single threaded server
using raw sockets and `listen(20)`. That seems like a reasonably large queue?
To be honest, I'm not *entirely* certain how that works - in the past I've used
huge numbers or smaller numbers and didn't really see a difference.
