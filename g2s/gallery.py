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


class GalleryFilesystem(object):
    def __init__(self, serializer):
        self._serializer = serializer

    @property
    def albums(self):
        albums = []
        with open('albums/albumdb.dat', 'r') as albumdb_dat:
            albumdb = self._serializer.loads(albumdb_dat.read())
        for album in albumdb:
            with open('albums/{}/album.dat'.format(album), 'r') as album_dat:
                albums.append(self._serializer.loads(album_dat.read()))
        return albums


class Serializer(object):
    def loads(self, data):
        def object_hook(name, d):
            name = name.lower()
            if name != 'album':
                raise TypeError('unknown type {}'.format(name))
            fields = d['fields']
            kwargs = {}
            kwargs['title'] = fields['name']
            if 'parentAlbumName' in fields:
                kwargs['parent'] = fields['parentAlbumName']
            return Album(**kwargs)

        loaded = phpserialize.loads(data, object_hook=object_hook)
        if isinstance(loaded, dict):
            loaded = phpserialize.dict_to_list(loaded)
        return loaded
