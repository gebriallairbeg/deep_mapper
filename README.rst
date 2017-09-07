# deep_mapper
could be used to turn one py-object (mash of dicts / lists etc) into another one,
using deep mapping structure and postprocessing through custom functions / builtins


mapping structure example
```
{
    'name': {
        'path': '/title'
        },
    'time': {
        'path': '/runtime',
        'postprocess': int
        },
    'restrictions': {
        'path': '/age_restricted'
        },
    'tags': {
        'path': '/tags/tag'
        },
    'image': {
        'path': '/gallery/image/@href'
        },
}
```
all pathes need to be based on XPath rules