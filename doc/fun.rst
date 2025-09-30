Fun and games
-------------

With |ISBN|-13 a book can have a valid checksum and have a simple transcription
error, if digits with a difference of five are transposed.

.. Maybe we need a ref, like ":title:`Design Patterns` [GoF95]_ is an excellent read."

Using :title:`The Statistical Mechanics of Financial Markets` as an example, we
can see that 9783540009788 is the `given ISBN`_, and is valid.  However,
97\ **38**\ 540009788 with the third and fourth characters transposed is also
valid, yet is incorrect [1]_.

I'll leave it as an exercise for the reader to figure out how often books with
transposable |ISBN|-13 occur in a given library of *n* books.

.. [1] This example was chosen to show that sometimes it is still possible to
       catch during data entry as 973 isn't a valid prefix

.. _given ISBN: https://books.google.com/books?vid=isbn:9783540009788

.. spelling:word-list::

   transposable
