import collections

import phpserialize

from . import util


class AlbumDict(object):
    def __init__(self, galleryfs):
        self._galleryfs = galleryfs

    def __getitem__(self, album_name):
        photos_dict = self._galleryfs.photos
        album = self._galleryfs.albums[album_name]
        album.photos = photos_dict[album_name]
        return album

    def items(self):
        return [(album_name, self[album_name])
            for album_name in self._galleryfs.album_names]


class Gallery(object):
    def __init__(self, galleryfs):
        self._galleryfs = galleryfs

    @property
    def albums(self):
        return AlbumDict(self._galleryfs)

    def iter_albums(self):
        return self.album_tree.iter_objects(0)

    @property
    def album_tree(self):
        tree = util.ParentNameTree()
        for name in self._galleryfs.album_names:
            tree.add_object(self._galleryfs.albums[name])
        return tree


class Album(object):
    def __init__(self, name, parent=None, title=None, description=None,
                 photos=[]):
        self.name = name
        self.description = description
        self.parent = parent
        self.title = title
        self.photos = photos

    @classmethod
    def from_fields(cls, fields):
        kwargs = {
            key: value for (key, value) in fields.iteritems()
            if key in ['name', 'title', 'description']
        }
        if 'parentAlbumName' in fields:
            kwargs['parent'] = fields['parentAlbumName']
        return cls(**kwargs)


class LazyLoadingDict(collections.defaultdict):
    '''Variation of defaultdict which passes the key to the default factory'''

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory(key)
        return value


class GalleryFilesystem(object):
    def __init__(self, serializer):
        self._serializer = serializer
        self._album_names = None

    @property
    def albums(self):
        def load_album(name):
            with open('albums/{}/album.dat'.format(name), 'r') as album_dat:
                return self._serializer.loads(album_dat.read())
        # Use a lazy loader so we can present a mapping interface for the
        # client, but don't have to load all of the albums on initialization
        return LazyLoadingDict(load_album)

    @property
    def photos(self):
        def load_photos(name):
            with open('albums/{}/photos.dat'.format(name), 'r') as photos_dat:
                return self._serializer.loads(photos_dat.read())
        # Use a lazy loader so we can present a mapping interface for the
        # client, but don't have to load all of the albums on initialization
        return LazyLoadingDict(load_photos)

    @property
    def album_names(self):
        if self._album_names is None:
            with open('albums/albumdb.dat', 'r') as albumdb_dat:
                albumdb = self._serializer.loads(albumdb_dat.read())
            self._album_names = albumdb
        return self._album_names


class Serializer(object):
    def loads(self, data):
        def object_hook(name, d):
            name = name.lower()
            if name == 'album':
                fields = d['fields']
                return Album.from_fields(fields)
            else:
                return phpserialize.phpobject(name, d)

        loaded = phpserialize.loads(data, object_hook=object_hook)
        if isinstance(loaded, dict):
            loaded = phpserialize.dict_to_list(loaded)
        return loaded
