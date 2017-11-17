import PIL

import shutil
import os

if not os.path.exists('./dist'):
    os.mkdir('dist')

if not os.path.exists('dist/PIL'):
    shutil.copytree(os.path.dirname(PIL.__file__), 'dist/PIL')
