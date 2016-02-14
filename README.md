# byobu-rpm
files to build an rpm for byobu
# Building the RPM
```
$ cd byobu-rpm
$ cp byobu_5.97.orig.tar.gz ~/rpmbuild/SOURCES
$ cp p ~/rpmbuild/SOURCES
$ rpmbuild -ba byobu.spec
```
the freshly built rpm is now in `~/rpmbuild/RPMS/noarch/`
