# Ansible Role: windows_msxml_install

Rôle Ansible to Delete MSXML on Windows

## General Information

**Author:** A&ECoding
**License:** MIT
**Minimum Ansible Version:** 2.9

**Supported Platforms:**
- Windows
  - Versions: all

## Variables

### main

```yaml
msxml_version: '6.0'
msxml_reinstall: false
cleanup_temp_files: true
allow_reboot: false

```

## Main Tasks

- Create PowerShell script for MSXML check
- Check if specified MSXML version already exists
- Set MSXML facts from check result
- Display MSXML status
- Create PowerShell script for MSXML download and installation
- Install MSXML if not found or reinstall is requested
- Parse installation result
- Display installation results
- Set reboot flag if required
- Verify installation after completion
- Display verification results
- Remove temporary PowerShell scripts
- Reboot system if required after MSXML installation

## Role Structure

```
defaults/
    └── main.yml
files/
handlers/
    └── main.yml
meta/
    └── main.yml
tasks/
    └── main.yml
templates/
tests/
    ├── inventory
    └── test.yml
vars/
    └── main.yml
README.md
```