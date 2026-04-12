Installs mktxp via pip into a Python virtualenv and manages it with systemd on the nft-monitor host.

The rendered mktxp.conf is built from hosts in the inventory group named by `mktxp_router_group`, which defaults to `network_switches`.
