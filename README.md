# Prefecture


1.  Add the source code directory to PATH: e.g. ``export PATH=$PATH:/home/blabla/blabla/blabla/prefecture/``
2. Install selenium: ``pip install -U selenium``
3. Run: ``python main.py --url https://www.essonne.gouv.fr/booking/create/23014/ --delay 5
`` (for testing purpose ``python main.py --url http://www.essonne.gouv.fr/booking/create/30986/ --delay 4``).

```
> python main.py -h
usage: main.py [-h] --url URL [--delay DELAY]

RDV Prefecture

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Link of the RDV webpage. e.g:
                        https://www.essonne.gouv.fr/booking/create/23014/
  --delay DELAY, -d DELAY
                        Delay in second between request.
```


NB: Increase the delay ``--delay`` if you encounter more "Bad gateway" error.
