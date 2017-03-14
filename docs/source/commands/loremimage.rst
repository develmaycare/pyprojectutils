loremimage
==========

Generate lorem image.

.. code-block:: none

    usage: loremimage [-h]
                      [-C= {abstract,animals,business,cats,city,food,nightlife,fashion,people,nature,sports,technics,transport,*}]
                      [--format= [{html,plain}]] [-H=--height= IMAGE_HEIGHT]
                      [-W= IMAGE_WIDTH] [-v] [--version]
                      display_text

    positional arguments:
      display_text          Text to display for alt and overlay.

    optional arguments:
      -h, --help            show this help message and exit
      -C= {abstract,animals,business,cats,city,food,nightlife,fashion,people,nature,sports,technics,transport,*}, --category= {abstract,animals,business,cats,city,food,nightlife,fashion,people,nature,sports,technics,transport,*}
                            The category of images to display.
      --format= [{html,plain}]
                            Choose the format of the output.
      -H=--height= IMAGE_HEIGHT
                            Height of the image.
      -W= IMAGE_WIDTH, --width= IMAGE_WIDTH
                            Width of the image.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.
