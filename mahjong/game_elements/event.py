

class Event(list):
    __slots__ = ('__weakref__',)

    def __call__(self, *args, **kwargs):
        for delegate in self[:]:
            delegate(*args, **kwargs)

    def __iadd__(self, delegate):
        if not callable(delegate):
            raise TypeError('Event listener is not callable.')

        if delegate not in self:
            self.append(delegate)
        return self

    def __isub__(self, delegate):
        if delegate in self:
            self.remove(delegate)
        return self

    def clear(self):
        del self[:]

    def __repr__(self):
        return 'Event({}): {}'.format(len(self), repr(self[:]))
