import os

from . import app
from . import gallery

class GalleryLoader(object):
    def __getitem__(self, directory):
        # This chdir isn't threadsafe, but that's fine as long as we stick
        # within the CLI and don't move to a web service
        os.chdir(directory)
        fs = gallery.GalleryFilesystem(gallery.Serializer())
        return gallery.Gallery(fs)

cli = app.CLI(GalleryLoader(), None)
