Evilshortgen
============
It's a best way to break your app =)

Your code without shortgen looks like::

    def fetch(arg1, arg2, callback):
        pass
    
    @tornado.gen.engine
    def get(self):
        value = yield tornado.gen.Task(fetch,
            arg1='arg1', arg1='arg2'
        )
        self.write(value)

But with shortgen evil magic::

    @fastgen
    def fetch(arg1, arg2, callback):
        pass

    @tornado.gen.engine
    @shortgen
    def get(self):
        value << fetch(
            arg1='arg1', arg1='arg2'
        )
        self.write(value)

Usage
=====
Call exist code like assyncmongo, patch and call with '_e'::

    from evilshortgen import shortgen, shortpatch
    from asyncmongo.cursor import Cursor
    shortpatch(Cursor)

    @tornado.gen.engine
    @shortgen
    def get(self):
        result, status << self.db.users.find_one_e({
            '_id': ObjectId(self.user_id),
            },
        )

Call new code with decorator::

    from evilshortgen import shortgen, fastgen

    @fastgen
    def fetch(arg1, arg2, callback):
        pass

    @tornado.gen.engine
    @shortgen
    def get(self):
        value << fetch(
            arg1='arg1', arg1='arg2'
        )

Known issues
============
Short calls set only values, not arguments::
    
    self.a << fetch()  # not work
    a << fetch()  # work

Group tuple assignment not work::
    
    (a, b), c << fetch()  # not work
    a, b, c << fetch()  # work
