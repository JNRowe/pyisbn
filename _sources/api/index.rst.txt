.. currentmodule:: pyisbn

API documentation
=================

Class based access
------------------

.. toctree::
   :maxdepth: 2

   isbn
   isbn10
   isbn13
   sbn

Exceptions
----------

.. autoexception:: pyisbn.CountryError

.. autoexception:: pyisbn.IsbnError

.. autoexception:: pyisbn.SiteError


Function based access
---------------------

Additionally the top-level functions are available, if you do not wish to use
the classes.

.. note::
   While the layout of this module is a result of it moving from a strictly
   function-based layout to a class-based layout these functions will not be
   removed.  Backwards compatibility is important, and will be maintained.

.. toctree::
   :maxdepth: 2

   func

Internal support features
-------------------------

.. toctree::
   :maxdepth: 2

   _constants
   _types
   _utils
