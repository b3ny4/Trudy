# Trudy
Trudy is a Network Intrusion Library.

### Tested on
 - Ubuntu 20.04 (Focal Fossa)
 - Ubuntu 22.04 (Jammy Jellyfish)

## DEPENDENCIES
This library relies on the pip modules in requirements.txt.

Some libraries get built by pip and require the following debain/ubuntu packets (tested on Ubuntu 22.04)

```
build-essential python-dev python3-dev libnetfilter-queue-dev
```

## Trudy
Trudy itself represents the attacker machine. You can set it up for a variety of attacks and perform tasks like sniffing

## Logger
Logger is a (hopefully) thread safe (but safe enough for hacking) way to make beautiful output on the terminal

## Network
A Network represents an acessible Ethernet network, or parts of it. Networks can be scanned for clients

## Client
A Client represents a participant of a network. Its ports can be scanned and it can be man-in-the-middled and exploitet.