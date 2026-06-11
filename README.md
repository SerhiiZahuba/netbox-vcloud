<div align="center">

# NetBox vCloud Plugin
### _Synchronize vCloud Director VMs into NetBox_

[![GitHub Repo stars](https://img.shields.io/github/stars/SerhiiZahuba/netbox-vcloud-sync-plugin?style=social)](https://github.com/SerhiiZahuba/netbox-vcloud-sync-plugin/stargazers)
![NetBox version](https://img.shields.io/badge/netbox-4.4.1-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-yellow)
![License](https://img.shields.io/github/license/SerhiiZahuba/netbox-vcloud-sync-plugin?color=green)

</div>

---

## Overview

**NetBox vCloud** is a NetBox plugin for synchronizing virtual machines from **vCloud Director** into NetBox.

---

## Installation

```bash
cd /opt/netbox/
source /opt/netbox/venv/bin/activate
pip install netbox-vcloud
python3 manage.py migrate netbox_cloudsync
```

## Settings

Add to `configuration.py`:

```python
PLUGINS = [
    "netbox_cloudsync",
]
```

## Development

Run tests locally:

```bash
pytest
```

Publish to PyPI from GitHub Actions by pushing a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```
