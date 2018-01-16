*******************************************************************************
Mobile process calculi for programming the blockchain
*******************************************************************************

This document provides extra background and serves as a companion to the
RChain-Architecture documentation


GETTING STARTED
======================

This project uses Sphinx (http://www.sphinx-doc.org/en/stable/index.html) to build
html that is published to Read the Docs. To run this documentation on your computer,
you should do the following:

Prerequisites
--------------------------------------------------------------------------------
* Python 2.6 or later
* git

Install Sphinx, etc
--------------------------------------------------------------------------------
For OSX/Linux users (based on instructions here: https://read-the-docs.readthedocs.org/en/latest/getting_started.html)

* From command line:
``sudo pip install sphinx``
``sudo pip install sphinx-intl``
``sudo pip install sphinxcontrib-bibtex``

For Windows users:

* http://www.sphinx-doc.org/en/stable/install.html#windows-install-python-and-sphinx

Get source code
--------------------------------------------------------------------------------
* git clone: https://github.com/rchain/mobile-process-calculi-for-blockchain.git

How to do the translated
--------------------------------------------------------------------------------
If the language you wanna to translate has not been added to the source code. Then you should follow the `Add new language` section to create a new language support files.

If it has been added, then you should use the Poedit(https://poedit.net/download) editor to translate the files in ./locale/<lang>/LC_MESSAGES.
After finishing translation, just commit your code and create a PR.

Add new language
--------------------------------------------------------------------------------
Assume you wanna to add a new language Japanese, then you can find the i18n code of Japanese is 'ja'.
* ``make gettext``
* ``sphinx-intl update -p _build/gettext -l ja``, then you will get these directories that contain po files:
  - ./locale/de/LC_MESSAGES/
  - ./locale/ja/LC_MESSAGES/
* Translate your po files under ./locale/<lang>/LC_MESSAGES/.
* make -e SPHINXOPTS="-D language='ja'" html
Then you will get the translated documentation in the _build/html directory.

Build and view html
--------------------------------------------------------------------------------
* In a terminal window, go to the cloned directory.
* ``make html``
* ``cd build/html``
* ``open index.html`` (open in web browser)
* Tip: each time you run ``make html``, just reload your browser to view changes
