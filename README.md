<div align="center">

# ☁️ NetBox CloudSync Plugin  
### _Synchronize vCloud Director VMs into NetBox_

[![GitHub Repo stars](https://img.shields.io/github/stars/SerhiiZahuba/netbox-vcloud-sync-plugin?style=social)](https://github.com/SerhiiZahuba/netbox-vcloud-sync-plugin/stargazers)
![NetBox version](https://img.shields.io/badge/netbox-4.4.1-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-yellow)
![License](https://img.shields.io/github/license/SerhiiZahuba/netbox-vcloud-sync-plugin?color=green)

</div>

---

## 🚀 Overview

**NetBox CloudSync** — is a plugin for automatic synchronization of virtual machines from **vCloud Director** to **NetBox** using ORM.
The plugin is designed to quickly and safely update VM data without manual intervention. 

---

## ⚙️ Installation

```bash
cd /opt/netbox/
source /opt/netbox/venv/bin/activate
git clone https://github.com/SerhiiZahuba/netbox-vcloud-sync-plugin.git
pip install -e .
python3 manage.py migrate netbox_cloudsync
```

## Settings

Add to configuration.py
```
PLUGINS = [
'netbox_cloudsync',
]
```

🔄 Features

🧰 Future Plans
