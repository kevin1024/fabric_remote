# Sample python command-line Fabric Remote Client


Here's an example client.  You can run it like this:

```
$ python cmdline.py --username admin --password secret --url http://localhost:1234 host_type
[192.168.100.188] Executing task 'host_type'
[192.168.100.188] run: uname -a
[192.168.100.188] out: Linux Thu Mar 14 12:45:00 EDT 2013 x86_64 x86_64 x86_64 GNU/Linux
[192.168.100.188] out:
```

