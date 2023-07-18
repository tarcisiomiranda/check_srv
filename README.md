## How to run

***Clone project***
```
git clone link.git /opt/check_srv
```

***Run command line***
```
python3 /opt/check_srv/check_srv.py --vg=docker --lv=srv
```

***Run every 6 hour***
```
0 */4 * * * root /usr/bin/python3 /opt/check_srv/check_srv.py --vg=docker --lv=srv >> /var/log/check_srv.log 2>&1
```
