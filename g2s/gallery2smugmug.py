from . import app
from . import gallery

class GalleryLoader(object):
    def __getitem__(self, directory):
        return gallery.GalleryFilesystem(directory=directory)

cli = app.CLI(GalleryLoader(), None)
