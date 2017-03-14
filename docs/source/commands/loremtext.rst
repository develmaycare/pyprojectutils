loremtext
=========

Generate lorem text.

.. code-block:: none

usage: loremtext [-h] [--format= [{html,plain}]] [--headings]
                 [--image-category= {abstract,animals,business,cats,city,food,nightlife,fashion,people,nature,sports,technics,transport,*}]
                 [--image-height= IMAGE_HEIGHT]
                 [--image-width= IMAGE_WIDTH] [--images]
                 [-s= TOTAL_SECTIONS] [-v] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      --format= [{html,plain}]
                            Choose the format of the output.
      --headings            Generate heading text.
      --image-category= {abstract,animals,business,cats,city,food,nightlife,fashion,people,nature,sports,technics,transport,*}
                            The lorempixel.com category of images when using
                            --images option. Use * for random.
      --image-height= IMAGE_HEIGHT
                            Height of images when using --images option.
      --image-width= IMAGE_WIDTH
                            Width of images when using --images option.
      --images              Generate images in the text. Uses lorempixel.com for
                            the image.
      -s= TOTAL_SECTIONS, --sections= TOTAL_SECTIONS
                            Number of sections to generate.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.
