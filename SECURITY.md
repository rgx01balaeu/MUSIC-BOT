# 🛡 Security Checklist

## 1. Authentication
- [x] Owner-only access to sensitive commands (`/adduser`, `/deluser`).
- [x] Whitelist system for private usage.
- [x] Callback query protection (only authorized users can trigger actions).

## 2. API Security
- [ ] Keep `API_ID` and `API_HASH` secret.
- [ ] Use environment variables for sensitive data.
- [ ] Regularly rotate `BOT_TOKEN` if exposed.

## 3. Bot Protection
- [ ] Anti-spam filters (Rate limiting).
- [ ] Flood wait handling (Pyrogram handles this automatically).
- [ ] Private chat restrictions.

## 4. VPS Security
- [ ] Disable root login via SSH.
- [ ] Use SSH keys instead of passwords.
- [ ] Configure a firewall (ufw) to allow only necessary ports (22, etc.).
