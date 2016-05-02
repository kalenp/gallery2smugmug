import phpserialize

from . import util

class Gallery(object):
    def __init__(self, galleryfs):
        self._galleryfs = galleryfs

    @property
    def albums(self):
        return self.album_tree.iter_objects(0)

    @property
    def album_tree(self):
        tree = util.ParentNameTree()
        for album in self._galleryfs.albums:
            tree.add_object(album)
        return tree


class Album(object):
    def __init__(self, title, parent=None):
        self.title = title
        self.parent = parent

    @property
    def name(self):
        '''Alias of title for compatibility with ParentNameTree'''
        return self.title


class GalleryLoader(object):
    def __getitem__(self, key):
        fs = GalleryFilesystem(key)
        return Gallery(fs)


def parse_albumsdb(albumsdb):
    return phpserialize.dict_to_list(phpserialize.loads(albumsdb))
