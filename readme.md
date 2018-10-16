# AutoMarkDocs

generate markdown docs from your python code automatically

combine with python-markdown for deploying to github pages right away!

files are imported and objects inspected, no source code parsing is done

samples docs for [ai_demos](https://jarbasal.github.io/ai_demos/)


# usage

    pip install pydoc-mardown
    
    cd /your/project
    git clone autmarkdocs 
    python autmarkdocs/automarkdocs.py
    pydocmd  build/serve/gh-deploy
    
# TODO

package and doc how to use args

maintain order in docs from which things are declared in files

auto create table of contents at page starts