# This script generates mkdocs friendly Markdown documentation from a python package.
# It is based on the the following blog post by Christian Medina
# https://medium.com/python-pandemonium/python-introspection-with-the-inspect-module-2c85d5aa5a48#.twcmlyack 
import inspect
import pydoc
import os, sys
from os.path import dirname, join
from pprint import pprint
from time import strftime

module_header = "# Package {} Documentation\n"
submodule_header = "\n## Module {}\n"
class_header = "\n###  {}\n"
function_header = "\n####  {}\n"
routine_header = "\n### {}\n"
comments_header = "NOTES:"


def get_module(module):
    if isinstance(module, str):
        sys.path.append(os.getcwd())
        # Attempt import
        module = pydoc.safeimport(module)
        if module is None:
            print("Module not found")
    return module


def get_markdown(module):
    module = get_module(module)

    output = [submodule_header.format(module.__name__)]
    if module.__doc__:
        output.append(module.__doc__)

    output.extend(get_classes(module))
    return "\n".join((str(x) for x in output))


def get_classes(item):
    item = get_module(item)
    output = list()
    for cl in pydoc.inspect.getmembers(item, pydoc.inspect.isclass):
        if cl[0] != "__class__" and not cl[0].startswith("_") and cl[ \
                1].__module__ == item.__name__:
            # Consider anything that starts with _ private
            # and don't document it
            output.append(class_header.format(cl[0]))
            # Get the docstring
            output.append(pydoc.inspect.getdoc(cl[1]))
            # Get the functions
            output.extend(get_methods(cl[1]))
            # Recurse into any subclasses
            output.extend(get_classes(cl[1]))
            output.append('\n\n')
    return output


def get_methods(item):
    item = get_module(item)
    output = list()
    # class methods (without self)
    try:  # fails wit hsqlalchemy (at least)
        for func in pydoc.inspect.getmembers(item, pydoc.inspect.getmembers):

            if func[0].startswith('_') or "built-in function" in str(func[1]):
                continue
            if isinstance(func[1], dict) or isinstance(func[1], int) or \
                    isinstance(func[1], list):
                continue

            try:
                if func[1].__module__ == item.__module__:
                    output.append(
                        function_header.format(func[0].replace('_', '\\_')))

                    # Get the signature
                    output.append('\n\n')
                    output.append('```\n')
                    output.append('def %s%s\n' % (
                        func[0], str(pydoc.inspect.signature(func[1]))))
                    output.append('```\n\n')
                    output += get_comments(func[1])

                    # get the docstring
                    if pydoc.inspect.getdoc(func[1]):
                        output.append('\n')
                        output.append(
                            "\n\n".join(pydoc.inspect.getdoc(func[1]).split(
                                "\n")))

                    output.append('\n')
            except:
                pass
    except:
        pass
    return output


def get_comments(item):
    item = get_module(item)
    comments = inspect.getcomments(item)
    output = []
    if comments:
        output.append(comments_header)
        output.append('\n')
        output.append(comments.replace("#", "").strip() + "\n")
    return output


def get_routines(item):
    item = get_module(item)
    output = list()
    for func in pydoc.inspect.getmembers(item, pydoc.inspect.isroutine):
        if func[0].startswith('_') or "built-in function" in str(func[1]):
            continue
        if item.__name__ == func[1].__module__:
            output.append(routine_header.format(func[0].replace('_', '\\_')))

            # Get the signature
            output.append('\n\n')
            output.append('```\n')
            output.append('def %s%s\n' % (
                func[0], str(pydoc.inspect.signature(func[1]))))
            output.append('```\n\n')
            output += get_comments(func[1])
            # get the docstring
            if pydoc.inspect.getdoc(func[1]):
                output.append('\n')
                output.append("\n\n".join(pydoc.inspect.getdoc(func[1]).split(
                    "\n")))

            output.append('\n')
    return output


def deep_docs(item):
    item = get_module(item)
    docs = get_markdown(item)
    docs += " ".join(get_routines(item))
    for cl in pydoc.inspect.getmembers(item, pydoc.inspect.ismodule):
        if not cl[0].startswith("_") and item.__name__ in str(cl[1]):
            # Recurse into any submds
            if item.__name__ != cl[1].__name__:
                docs += "\n" + deep_docs(cl[1])
    return docs


def generate_docs(module):
    try:
        module = get_module(module)

        # Module imported correctly, let's create the docs
        doc = module_header.format(module.__name__)
        # Markdown title line

        doc += deep_docs(module)
        return doc
    except pydoc.ErrorDuringImport as e:
        print("Error while trying to import " + str(module))


def generate_pydocmd(module, docs_path="/docs"):
    module = get_module(module)
    pydocmd_str = "site_name: " + module.__name__
    pydocmd_str += "\ngenerate:"
    path = join(dirname(docs_path), "_build/pydocmd")
    pydocmd_str += "\ngens_dir: " + path
    path = join(dirname(docs_path), "_build/site")
    pydocmd_str += "\nsite_dir: " + path
    pydocmd_str += "\npages:"
    path = join(dirname(docs_path), "readme.md")
    pydocmd_str += "\n- Home: index.md << " + path

    tree = generate_module_tree(module)

    def link_docs(bucket):
        nonlocal pydocmd_str
        for k in bucket:
            n = len(k.split(".")) - 2

            d = bucket[k]
            path = join(docs_path, k.replace(".", "/"))
            if isinstance(d, dict):
                pydocmd_str += "\n" + n * "  " + "- " + k.split(".")[-1] + ":"
                path = "\n" + (n + 1) * "  " + "- " + k.split(".")[-1] + ": " \
                       + k + ".md" + " << " + join(path, k + ".md")
                pydocmd_str += path
                link_docs(d)
            else:
                path = "\n" + n * "  " + "- " + k.split(".")[-1] + ": " + k \
                       + ".md" + " << " + join(path, k + ".md")
                pydocmd_str += path

    link_docs(tree)

    return pydocmd_str


def generate_module_tree(item):
    item = get_module(item)

    submodules = []
    try:
        path = list(item.__path__)[0]
        submodules = [item.__name__ + "." + o for o in os.listdir(path) if
                      os.path.isdir(
                          os.path.join(path, o)) and not o.startswith("_")]

        files = [item.__name__ + "." + o.replace(".py", "") for o in
                 os.listdir(path) if
                 o.endswith(".py") and not o.startswith("_")]
    except:
        files = []
    modules = {}
    for m in files:
        modules[m] = ""
    for m in submodules:
        modules[m] = generate_module_tree(m)
    return modules


def create_doc_folder(module, docs_path="docs"):
    print("mapping module:", module)
    tree = generate_module_tree(module)
    pprint(tree)
    base_path = os.path.join(docs_path, module)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    print("making directories", base_path)
    print("docs dir:", docs_path)
    def make_dirs(bucket):
        for k in bucket:
            d = bucket[k]
            path = os.path.join(docs_path, k.replace(".", "/"))
            if not os.path.exists(path):
                os.makedirs(path)
                print("created", path)
            if isinstance(d, dict):
                make_dirs(d)

            # else:
            print("generating docs for", k)
            path = os.path.join(path, k + ".md")
            with open(path, "w") as f:

                doc_str = add_spaces(deep_docs(k))
                f.write(doc_str)

    make_dirs(tree)


def add_spaces(text, n=0):
    lines = text.split("\n")
    for idx, l in enumerate(lines):
        if l.strip().startswith("#") or l.strip().startswith(comments_header):
            continue
        lines[idx] = n * " " + l
    return "\n".join(lines)


if __name__ == '__main__':
    import argparse

    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--module', '-m', required=False, action='store',
                            help='Source folder containing python files.')
    arg_parser.add_argument('--docfile', '-o', required=False, action='store',
                            help='Docs folder to write output to.')

    args = arg_parser.parse_args()

    docs_path = args.docfile or "../docs"
    module = args.module or os.path.dirname(__file__).split("/")[-1]

    create_doc_folder(module, docs_path)

    pydocmd = generate_pydocmd(module, docs_path)

    item = get_module(module)
    path = os.path.join(docs_path, "pydocmd.yml")
    with open(path, "w") as f:
        f.write(pydocmd)
