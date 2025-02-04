# hacs-nature-remo

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

| Platform        | Description                                                               |
| --------------- | ------------------------------------------------------------------------- |
| `binary_sensor` | Show something `True` or `False`.                                         |
| `sensor`        | Show info from hacs-nature-remo API. |
| `switch`        | Switch something `True` or `False`.                                       |

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `hacs_nature_remo`.
4. Download _all_ the files from the `custom_components/hacs_nature_remo/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "hacs-nature-remo"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/hacs_nature_remo/translations/en.json
custom_components/hacs_nature_remo/translations/fr.json
custom_components/hacs_nature_remo/translations/nb.json
custom_components/hacs_nature_remo/translations/sensor.en.json
custom_components/hacs_nature_remo/translations/sensor.fr.json
custom_components/hacs_nature_remo/translations/sensor.nb.json
custom_components/hacs_nature_remo/translations/sensor.nb.json
custom_components/hacs_nature_remo/__init__.py
custom_components/hacs_nature_remo/api.py
custom_components/hacs_nature_remo/binary_sensor.py
custom_components/hacs_nature_remo/config_flow.py
custom_components/hacs_nature_remo/const.py
custom_components/hacs_nature_remo/manifest.json
custom_components/hacs_nature_remo/sensor.py
custom_components/hacs_nature_remo/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

---

[buymecoffee]: https://www.buymeacoffee.com/kkiyama117x
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/kkiyama117/hacs-nature-remo2.svg?style=for-the-badge
[commits]: https://github.com/kkiyama117/hacs-nature-remo/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/kkiyama117/hacs-nature-remo2.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40kkiyama117-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/kkiyama117/hacs-nature-remo2.svg?style=for-the-badge
[releases]: https://github.com/kkiyama117/hacs-nature-remo2/releases
[user_profile]: https://github.com/kkiyama117
