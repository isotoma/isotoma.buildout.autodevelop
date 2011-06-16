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

import os


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


def load(buildout):
    # build a list of buildout managed directories to *not* check for develop eggs
    # use realpath to make sure they are in an expected and consistent format
    ignore_list_vars = ("parts-directory", "develop-eggs-directory", "eggs-directory", "bin-directory", "download-cache")
    ignore_list = []
    for ignore in ignore_list_vars:
        ignore_list.append(os.path.realpath(buildout["buildout"][ignore]))

    # Allow the user to provide specific directories to autodevelop, and cope with whitespace at beginning, middle or end
    # Default to scanning current working directory
    to_develop = []
    for line in buildout["buildout"].get("autodevelop", ".").strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        to_develop.extend(search_directory(os.path.realpath(line), ignore_list))

    # Don't overwrite any develop values that were set manually
    develop = buildout["buildout"].get("develop", "")
    if develop:
        to_develop.append(develop)

    # Apply config tweaks
    buildout["buildout"]["develop"] = "\n".join(to_develop)


from zc.buildout.easy_install import Installer, pkg_resources

def _satisfied(self, req, source=None):
    versions = []

    dists = [d for d in self._env[req.project_name]]
    if filter(lambda d: d.precedence == pkg_resources.DEVELOP_DIST, dists):
        versions = filter(lambda s: s[0] == "==", req.specs)

        req.specs = filter(lambda s: s[0] != "==", req.specs)
        copy = pkg_resources.Requirement.parse(str(req))
        req.index = copy.index

    dist, avail = self._old_satisfied(req, source)

    if versions:
        dist._version = versions[0][1]

    return dist, avail

Installer._old_satisfied = Installer._satisfied
Installer._satisfied = _satisfied


