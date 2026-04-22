# NetFusion Unbound DNS Templates

## Standard Internal Host (.net)

```
Host: <name>
Domain: netfusiontechnologies.net
Type: A
IP Address: <IPv4>

Optional:
Type: AAAA
IP Address: <IPv6>

✔ Enable PTR record
```

---

## nginx Edge Entry (Anchor)

```
Host: edge
Domain: netfusiontechnologies.xyz
Type: A
IP Address: 192.168.54.10

Optional:
Type: AAAA
IP Address: <IPv6>
```

---

## nginx Alias (Public/Admin)

```
Alias: <service>.netfusiontechnologies.xyz
→ points to edge.netfusiontechnologies.xyz
```

Examples:

```
grafana.netfusiontechnologies.xyz
vme3.netfusiontechnologies.xyz
```

---

## Direct Service (No nginx)

```
Host: <service>
Domain: netfusiontechnologies.net
Type: A
IP Address: <service IP>

Optional AAAA
✔ Enable PTR
```

---

## Mail Service (Special Case)

```
Host: mail
Domain: netfusiontechnologies.com
Type: A
IP Address: <mail IP>

Optional AAAA

❗ Do NOT use CNAME
❗ Always use direct IP
```

---

## Rules

* `.net` = authoritative internal identity
* `.xyz` = nginx entrypoints
* `.com` = client-facing
* No `.net` → nginx
* No CNAME for mail
