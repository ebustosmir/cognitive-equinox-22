$TTL    604800
@       IN      SOA     ns1.cognitive-equinox.com. root.cognitive-equinox.com. (
                  3       ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; name servers - NS records
     IN      NS      ns1.cognitive-equinox.com.

; name servers - A records
ns1.cognitive-equinox.com.          IN      A      172.20.0.2

host5.cognitive-equinox.com.        IN      A      172.20.0.8
host2.cognitive-equinox.com.        IN      A      172.20.0.5
host3.cognitive-equinox.com.        IN      A      172.20.0.6
host4.cognitive-equinox.com.        IN      A      172.20.0.7
host1.cognitive-equinox.com.        IN      A      172.20.0.4
