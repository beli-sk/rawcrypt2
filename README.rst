Rawcrypt 2
====================

Simple data encryption tool which aims to produce output indistinguishable from
random data.


Operation details
-----------------

Uses AES in GCM mode with 256-bit key derived from password and random salt
using PBKDF2 with SHA-256.

Random salt and IV are prepended and GCM tag is appended to the encrypted data.

Uses cryptography_ Python library, which in turn uses OpenSSL backend.

.. _cryptography: https://cryptography.io


Locations
---------

The `project page`_ is hosted on Github.

If you find something wrong or know of a missing feature, please
`create an issue`_ on the project page. If you find that inconvenient or have
some security concerns, you could also contact me by come means described at
my `home page`_.

.. _project page:    https://github.com/beli-sk/rawcrypt2
.. _create an issue: https://github.com/beli-sk/rawcrypt2/issues
.. _home page:       https://beli.sk


License
-------

Copyright 2017 Michal Belica <https://beli.sk>

::
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

A copy of the license can be found in the ``LICENSE`` file in the
distribution.

