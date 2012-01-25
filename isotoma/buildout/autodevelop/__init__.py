# Copyright 2010 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys, subprocess
import zc.buildout.easy_install

import logging
logger = logging.getLogger(__name__)

def get_version(path, python=sys.executable):
    p = subprocess.Popen([python, "setup.py", "-V"], stdout=subprocess.PIPE, cwd=path)
    o, e = p.communicate()
    return o.strip()

def get_name(path, python=sys.executable):
    p = subprocess.Popen([python, "setup.py", "--name"], stdout=subprocess.PIPE, cwd=path)
    o, e = p.communicate()
    return o.strip()

def localegg(path, python=sys.executable):
    path = os.path.realpath(path)
    name = get_name(path, python=python)
    version = get_version(path, python=python)
    p = subprocess.Popen(["python2.4", "setup.py", "sdist", "--formats=zip"], cwd=path)
    p.communicate()
    return os.path.join(path, "dist", "%s-%s.zip" % (name, version))


def search_directory(dir, ignore_list):
    # build a list of eggs we can develop by looking for "setup.py"
    to_develop = []
    for path, dirs, files in os.walk(dir):

        # recurse through symlinks
        for d in dirs:
            dirpath = os.path.join(path, d)
            if os.path.islink(dirpath):
                to_develop.extend(search_directory(dirpath, ignore_list))

        # Don't look for eggs in ignored directories
        if os.path.realpath(path) in ignore_list:
            dirs[:] = [] # this is bizarre python for emptying a list in a way that os.walk can react to
            continue

        #  we don't descend into directories containg a setup.py
        if "setup.py" in files:
            to_develop.append(path)
            dirs[:] = []

    return to_develop


def split(lst):
    for itm in lst.strip().split('\n'):
        if itm.strip():
            yield itm.strip()


def load(buildout):
    mode = buildout.get("autodevelop", {}).get("mode", "checkout")
    if not mode in ("checkout", "localeggs", "deploy"):
        return

    buildout['autodevelop']['developed'] = ''

    # build a list of buildout managed directories to *not* check for develop eggs
    # use realpath to make sure they are in an expected and consistent format
    ignore_list_vars = ("develop-eggs-directory", "eggs-directory", "bin-directory", "download-cache")
    ignore_list = []
    for ignore in ignore_list_vars:
        var = buildout['buildout'].get(ignore, '')
        if var:
            ignore_list.append(os.path.realpath(var))

    # Add each of the parts directories to the list of ignored directories
    parts = split(buildout["buildout"]["parts"])
    parts_dir = buildout["buildout"]["parts-directory"]
    for part in parts:
        ignore_list.append(os.path.join(parts_dir, part))

    logger.debug("Not searching for packages in %s" % ", ".join(ignore_list))

    # The search directories are either ${autodevelop:directories}, ${buildout:autodevelop}, ${buildout:cwd} or '.'
    search_directories = buildout.get("autodevelop", {}).get('directories', \
        buildout["buildout"].get("autodevelop",  \
        buildout['buildout'].get('cwd', \
        buildout['buildout']['directory'])))

    # Search the search directories. Cope with withspace and stuff.
    to_develop = []
    for line in split(search_directories):
        to_develop.extend(search_directory(os.path.realpath(line), ignore_list))

    # Don't overwrite any develop values that were set manually
    develop = list(split(buildout["buildout"].get("develop", "")))
    if develop:
        to_develop.extend(develop)

    # We reverse sort based on the path to the develop eggs. This way we have a consistent ordering that
    # is compatible with zope.testing.testrunner
    to_develop.sort(reverse=True)

    if mode == "checkout":
        # Apply config tweaks
        buildout["buildout"]["develop"] = "\n".join(to_develop)
        buildout["autodevelop"]['developed'] = "\n".join([get_name(d) for d in to_develop])

    if mode == "localeggs":
        find_links = list(split(buildout.get('find-links', '')))
        find_links.extend([localegg(path) for path in to_develop])
        buildout["buildout"]["find-links"] = '\n'.join(find_links)

    buildout._raw.setdefault("versions", {})
    buildout._raw["versions"].update(
        dict((get_name(path), get_version(path)) for path in to_develop))

    zc.buildout.easy_install.default_versions(buildout._raw["versions"])

