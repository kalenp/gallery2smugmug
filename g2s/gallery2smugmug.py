from . import app
from . import gallery

cli = app.CLI(gallery.GalleryLoader, None)
