# SSH Key Policy (Proxmox Hosts)

## Scope
- Applies to all Proxmox hosts (LAN-only SSH).
- No secrets or real keys in repo; only example placeholders.
- Goal: key-based access, safe by default (no unintended lockouts).

## Defaults
- `ssh_allowed_keys`: example keys only; replace with your own.
- `ssh_keys_enforce`: `false` by default (does **not** remove existing keys).
- `authorized_keys_path`: managed path (typically `/root/.ssh/authorized_keys`, often symlinked to `/etc/pve/priv/authorized_keys` in Proxmox clusters).

## Behavior
- When `ssh_keys_enforce: false` (default):
  - Ensures allowed keys exist.
  - Does **not** remove other keys (safe mode).
- When `ssh_keys_enforce: true` (opt-in):
  - Replaces `authorized_keys` with `ssh_allowed_keys` (removes others).
  - Playbook fails early if enforcement is enabled but the allowed list is empty (prevents lockout).

## Operational Guidance
- Before enabling enforcement:
  - Populate `ssh_allowed_keys` with all required keys.
  - Keep a console/ILO session open while applying changes.
  - Verify new SSH login in a separate session before closing the old one.
- If you rely on Proxmox’s shared `authorized_keys` (symlink to `/etc/pve/priv/authorized_keys`):
  - Enforcement affects the cluster-wide file; ensure the allowed list is complete across all admins.

## TODO
- Define process for rotating keys (who, when, where to PR).
- Decide retention of historical keys and audit trail location.

