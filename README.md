# freifunk client monitor

```
ip addr flush dev wlan0
rfkill block wlan
sleep 5
rfkill unblock wlan
```

Logge:

* Uhrzeit
* Ist SSID 'Freifunk' sichtbar?
* IPv4 nach dhclient und 20sec
* IPv6
* Ping und latenz nach remote host im Internet

