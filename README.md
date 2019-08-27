# RPKI Origin Validation Tutorial

***SAFNOG-5, JNB, August 2019***

Sources for the tutorial to be held at SAFNOG-5 on Tuesday, 27 August
16:00 - 17:30 SAST.

## Prerequisites

### Docker Host

You will need a linux machine (or VM). The following intructions assume that
the host is running **Ubuntu 18.04**.

The steps described may need to be adapted for other distrobutions and/or
versions.

### Host firewall

Docker doesn't manage `ip6tables` config, like it does for IPv4. IPv6 ND is
broken as a result. To permit bridged traffic (using `ufw`) add the following
to `/etc/ufw/user6.rules`:

```
-A ufw6-user-forward -m physdev --physdev-is-bridged -j ACCEPT
```

... and then

```bash
sudo ufw reload
```

### Docker

The lab is implemented as an interconnected set of docker containers.
Orchestration is handled by docker compose.

### Juniper cRPD

The routers in the lab topology run Juniper cRPD, a containerised version of
the Junos routing protocol daemon. We can't distribute that here for licensing
reasons, so you need to get that elsewhere.

The lab has been tested using version `19.2R1.8`, but others should work
with some adjustments.

Once you have obtained a tarball of the image, load into the local image repo
with:

```bash
$ docker load -i crpd-19.2R1.8.tgz
```

## Topology

The lab topology looks like:

```
  j1       j2 ---- t1
   |       |
 -------------
  |    |    |
 ccc  rp1  rp2
```

`j1` and `j2` are routers in AS65000. They speak IS-IS and iBGP for both IPv4
and IPv6 unicast address families.

`t1` is a route injector (running exabgp) emulating a transit provider (AS65001), attached to
`j2`.

The routers are also attached to a management network containing  - `ccc`.

Also on the internal network are two rpki validation caches and the config
management machine:
- `rp1` runs the ripe validation cache version 3.1.
- `rp2` runs routinator version xxx.

## Usage

To launch, just do:

```bash
$ docker-compose up
```

If you have made changes to the sources, then rebuild the docker images with:

```bash
$ docker-compose build
```

See the `docker-compose` docs for more usage info.
