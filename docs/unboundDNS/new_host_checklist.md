# NetFusion DNS – Add Host/Service Checklist

## 1. Determine Role

Choose the correct prefix:

* Physical / infrastructure → `nft-`
* VM / container → `vm-`
* Database → `db-`
* Shared service → `svc-`
* Infrastructure component → `infra-`
* Automation platform → `auto-`
* Application → `app-`

---

## 2. Assign Canonical Name (.net)

Create the authoritative identity:

```
<name>.netfusiontechnologies.net
```

---

## 3. Assign IP Address

* Static or reserved via KEA
* Ensure no conflicts
* Document VLAN/subnet

---

## 4. Create Unbound Host Override

* Add A record (IPv4)
* Add AAAA record (IPv6) if used
* Enable PTR record

---

## 5. Decide Access Method

* Internal only → `.net`
* Admin/public via nginx → `.xyz`
* Client-facing → `.com`

---

## 6. Configure nginx (if needed)

* Add virtual host
* Route to backend `.net` hostname

---

## 7. Validate

Test:

```
dig <fqdn>
ping <fqdn>
```

From:

* LAN
* VPN
* External (if applicable)

---

## 8. Optional: Search Domains

* Configure via KEA or Ansible if short names required

---

## Summary

* `.net` = internal identity
* `.xyz` = admin/public access
* `.com` = client-facing
* Unbound = DNS authority
* KEA = IP assignment
