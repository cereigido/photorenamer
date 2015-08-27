photorenamer
============

> For an obsessive-compulsive disorder <del>programmer</del> person who likes to order pictures by its original date and time.

- Run from current or choose the desired dir 
- Pictures will be renamed according to it's original creation time (stamped on file by most cameras) or its checksum
- Optionally, files with no camera creation date info can be named by the date and time the were created on disk
- File pattern will something like YYYYMMDD-HHMMSS-HASH.ext

Installation
------------

```sh
pip install git+https://github.com/cereigido/photorenamer.git
```

Usage
-----

```sh
python photorenamer.py [-h] [-p PATH] [-v]
```

Arguments
---------

-  -p PATH, --path PATH
  - Path containing images to be renamed
-  -v, --verbose
  - Verbose mode


What's (maybe) next?
--------------------

- Allow date time editing
- Allow recursive renaming

License
-------

MIT
