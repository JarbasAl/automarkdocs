# AutoMarkDocs
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)

generate markdown docs from your python code automatically

combine with python-markdown for deploying to github pages right away!

files are imported and objects inspected, no source code parsing is done

samples docs for [ai_demos](https://jarbasal.github.io/ai_demos/)


# usage

    pip install pydoc-markdown
    
    git clone https://github.com/JarbasAl/automarkdocs
    cp autmarkdocs/automarkdocs.py /your/project/automarkdocs.py
    
    cd /your/project
    python ./automarkdocs.py
    
    pydocmd build
    pydocmd serve
    pydocmd gh-deploy
    
# TODO

package and doc how to use args

maintain order in docs from which things are declared in files

auto create table of contents at page starts
