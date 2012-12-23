geoip_tool
==========

PHP tool for Geo IP configuration

This uses YAML configuration file, parsed via [Spyc](https://github.com/mustangostang/spyc).

Configuration File (geo.db):
----------------------------

    countries:
      - default:
          url: http://revelsystems.com/
      - admin:
          IP:
            - 75.94.141.120/32 #chris
            - 96.24.78.238/32 #chris
            - 178.165.58.116/32 #max
          url: /wp-admin/
      - Ukraine:
          hostip_service: true
          url: http://www1.revelsystems.com/
      - Australia:
          hostip_service: true
          IP:
            - 218.185.232.0/24
            - 216.220.208.0/24
          url: http://au.revelsystems.com/

Rules matching behavior:
------------------------

- Tool looks for exact IP match (with CIDR `32`).
- Then IPs with `24`, `16` and `8` CIDR are checked.
- If `hostip_service` is set to true:
  - checks `hostip.info` webservice for the country name using [APIs](http://www.programmableweb.com/api/hostip.info)
- Uses default settings.

Limitations:
------------

- Each section is required to have `url` parameter (either absolute or relative).
- CIDR mask is required for IP addresses.
- Do not use CIDR mask different from `8`, `16`, `24` or `32`.
- Geo IP tool uses configuration file `geo.db` located the same directory as `geo.php`.
- All configurations should be done under `countries` parent section.
