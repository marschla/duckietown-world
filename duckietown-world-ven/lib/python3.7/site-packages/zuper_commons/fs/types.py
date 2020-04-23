__all__ = [
    "Path",
    "AbsPath",
    "RelPath",
    "AbsDirPath",
    "AbsFilePath",
    "RelDirPath",
    "RelFilePath",
    "DirPath",
    "FilePath",
]

# Path = NewType("Path", str)
# AbsPath = NewType("AbsPath", Path)
# RelPath = NewType("RelPath", Path)
# AbsDirPath = NewType("AbsDirPath", AbsPath)
# AbsFilePath = NewType("AbsFilePath", AbsPath)
# RelDirPath = NewType("RelDirPath", RelPath)
# RelFilePath = NewType("RelFilePath", RelPath)
#
# DirPath = Union[AbsDirPath, RelDirPath]
# FilePath = Union[AbsFilePath, RelFilePath]
# DirEntryName = NewType("DirEntryName", RelPath)

AbsPath = AbsFilePath = AbsDirPath = str
Path = DirPath = FilePath = str
RelPath = RelDirPath = RelFilePath = str
