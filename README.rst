Autodevelop buildout extension
==============================

This package provides a buildout_ extension for automatically developing source eggs
in the current project.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Logging your buildout run
-------------------------

You just need to add an extension to your buildout.cfg::

    [buildout]
    extensions = isotoma.buildout.autodevelop

By default this will check every directory below where you execute buildout for
setup.py. Buildout managed directories like develop-eggs-directory will be excluded.
If you want to further restrict the search path, you can till the extension where
to search::

    [buildout]
    extensions = isotoma.buildout.autodevelop
    autodevelop =
        src
        externals

This will develop any source eggs contained in your src and externals directories.


Optional Parameters
-------------------

autodevelop
    If you don't want to scan the entire checkout, provide a subfolder to check


Repository
----------

This software is available from our `recipe repository`_ on github.

.. _`recipe repository`: http://github.com/isotoma/recipes


License
-------

Copyright 2010 Isotoma Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


