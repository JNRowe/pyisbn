Fun and games
-------------

With :abbr:`ISBN (International Standard Book Number)`-13 a book can have
a valid checksum and have a simple transcription error, if digits with
a difference of five are transposed.

Using "The Statistical Mechanics of Financial Markets" as an example, we can see
that 9783540009788 is the `given ISBN`_, and is valid.  However,
9738540009788 with the third and fourth characters transposed is also valid, yet
is incorrect[1]_ .

I'll leave it as an exercise for the reader to figure out how often books with
transposable :abbr:`ISBN (International Standard Book Number)`-13 occur in
a given library of ``n`` books.

.. [1] This example was chosen to show that sometimes it is still possible to
       catch during data entry as 973 isn't a valid prefix

.. _given ISBN: http://books.google.no/books?vid=isbn:9783540009788&redir_esc=y
