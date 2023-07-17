## How to run
***Run command line***
```
python3 /caminho/para/check_srv.py --vg=docker --lv=srv
```

***Run every 6 hour***
```
0 */6 * * * python3 /caminho/para/check_srv.py.py --vg=docker --lv=srv >> /var/log/check_srv.log 2>&1
```
