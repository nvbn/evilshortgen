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
