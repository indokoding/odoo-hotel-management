# Hotel Management System

This addon provides a hotel management system for Odoo.

## Requirements

- Odoo 16.0 Community Edition
You can find the Odoo installation instructions from [here](https://www.odoo.com/documentation/16.0/administration/install/source.html).

## Installation

1. Clone this repository.
```bash
git clone https://github.com/indokoding/odoo-hotel-management.git
```

2. Run the server using run command.
<details>
    <summary>Linux & MacOS</summary>

        cd /CommunityPath
        python3 odoo-bin --addons-path=addons,/customAddonsPath -d mydb
</details>
<details>
    <summary>Windows</summary>
    
        cd CommunityPath/
        python odoo-bin -r dbuser -w dbpassword --addons-path=addons,customAddonsPath -d mydb
</details>

Alternatively you can add the addons path to the Odoo configuration file before running the server.
```conf
addons_path = addons,/customAddonsPath
```
Note : _All the_ `customAddonsPath` _in this documentation should be replaced with your actual path._

## Usage

1. After logged in as admin, go to "Apps" menu.
2. Search for "Hotel Management System" addon.
3. Install the addon.
* The user guide can be found in **"Module Info"** inside dropdown menu by clicking the three dots on the top right of the addon.

## Credits

- Author: [CV. Indokoding Sukses Makmur](https://indokoding.com)
- Contributor: [Ahmad Husein Hambali](https://github.com/ucencode)
