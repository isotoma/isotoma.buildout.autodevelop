Autodevelop buildout extension
==============================

This package provides a buildout_ extension for automatically developing source eggs
in the current project.

You might also want to look at mr.developer which does a similar job but also
manages your SCM interactions, which autodevelop explicitly does NOT do.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Finding your develop eggs automatically
---------------------------------------

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


Testing 'real' eggs automatically
---------------------------------

We package all our eggs and deploy from a local PyPI mirror. It's useful to be
able to automatically run the egg build and test the buildout with that egg,
rather than the checkout. You will flush out your MANIFEST problems if you make
use of this.

You need to put the extension into 'localeggs' mode::

    [buildout]
    extensions = isotoma.buildout.autodevelop

    [autodevelop]
    mode = localeggs

Under the hood, the extension will call ``python setup.py sdist`` for each egg
that would have been developed and rewrites ``${buildout:find-links}`` to use
that.


Automatic version numbers
-------------------------

You probably won't want this, its a bit of an edge case.

If you are deploying from an SVN tag that contains your source code but you
want the deployment to use eggs from your PyPI mirror anyway then autodevelop
can automatically update the pins in your buildout to match the version of the
code in your tag, by rewriting the [versions] section of your config.

This looks like this::

    [buildout]
    extensions = isotoma.buildout.autodevelop

    [autodevelop]
     mode = deploy


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


