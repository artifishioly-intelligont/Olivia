class Lock:
    busy = False

    def lock(self):
        self.busy = True

    def unlock(self):
        self.busy = False

    def is_locked(self):
        return self.busy
