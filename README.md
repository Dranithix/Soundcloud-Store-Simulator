Soundcloud-Store-Simulator
==========================

A vague Python v3.3 implementation of a music store which plays/downloads tracks through the SoundCloud API.

PyQT 5 is used as the GUI Framework for this program, and all account data and the likes are stored via Text. The entire project was done within 3 days within my Junior year of high school.

In order to setup and run this simulator, simply install the PyQT5 bindings located inside the Git and insert a proper SoundCloud API key within main.py. Afterwards, run main.py and everything should work out.

Under the case of there being thrown exceptions due to the byte decoding of the JSON data provided from the SoundCloud API, simply decode the 'database' string on main.py (line 235) with UTF-8 encoding.
