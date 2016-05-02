class Album(object):
    def __init__(self, title, depth, albums=[]):
        self.title = title
        self.depth = depth
        self.albums = albums
