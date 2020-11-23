from setup import __version__ as version
from setup import __name__ as name

DOC_PATH = f'./docs/{name}.env'

def add_version(n, v):
    version_info = f'# {n}.env ---> Version: {v}'
    with open(DOC_PATH, 'a')  as doc:
        doc.write(version_info)

if __name__ == '__main__':
    add_version(name, version)
