# gallery2smugmug

Utility to transfer PHP Gallery 1.5 photos to SmugMug.

## Installation

* `git clone` the repository from github
* `make`.  This will set up a virtual environment and install necessary
  dependencies.

## Usage

```shell
$ gallery2smugmug --help

Usage:
  gallery2smugmug list [--gallery-path=<directory>]

  gallery2smugmug view <album> [--gallery-path=<directory>]

  gallery2smugmug upload [--api_key=<api_key>]
                         [--nick=<nickname>]
                         [--gallery-path=<directory>]
                         [--dry-run]

  gallery2smugmug forget [--nickname=<nickname>]
                         [--api-key]
```

The first time you upload with `gallery2smugmug`, you will be prompted to
authorize the tool by visiting a URL.  Once this has been done, the credentials
will be cached for future use.  To clear the cache, use the `forget` subcommand.

## Behavior

Gallery had the capability to have nested albums, which is unavailable in
SmugMug.  To handle this limitation, imported albums will be flattened to their
single parent.  The child album names will be added to the image keywords so
that they can be retrieved for later processing.
