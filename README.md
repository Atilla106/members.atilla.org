Contributing
---

If you are planning to contribute to the project, please check out our [contribution guide](https://gitlab.atilla.org/atilla/members/blob/dev/CONTRIBUTING.md) first.

Installation
---
This project is using Python 3 and Django in the most part, but also SASS (Ruby) for easy CSS rendering. Before diving into the project, make sure to have the following packages installed on your system : 

- For Python :
	- `python3`
	- `python-pip`
	- `virtualenv`
- For Ruby and SASS :
	- `ruby`
	- `ruby-gem` (often provided with the `ruby` package)

**Note : ** If you don’t need to compile SASS, you probably don’t need to install Ruby and its Gems.

Clone the project and set-up the Python environment :

- `git clone <repo url>`
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

If needed, set-up the Ruby environment :

- `gem install bundler`

If you get the following warning : `You don't have $HOME/.gem/ruby/X.X.X/bin in your PATH, gem executables will not run.`, you may need to include this very folder at the end of your $PATH variable.

`bundler`works a bit like `virtualenv`, but it uses a home folder to store your custom environment, you can override this option and store the gems of a bundle in your `venv` by providing the argument `--path=venv/rails` when running `bundle install`.

- Install the project Gems : `bundle install`

Once the Ruby setup is done, SASS should be compiled on-the-fly by the Django server.

Configuration
---

- Copy the exemple file `members/localSettings.py.example` to `members/localSettings.py`

- Set your LDAP credentials in `members/localSettings.py`

- Review the project settings in `members/settings.py`

Synchronize DHCP and DNS configuration
----

The script provided in `misc/update-network.sh` allows to update the DHCP and DNS configuration of a server running Debian Stretch. In production, this script should be executed as a cron job.

Update switches configuration
---

The platform provides an interface to update 802.1x configuration of switches.
Note that this only works on switches that have a telnet adapater corresponding to their model.

Currently, the platform only provides a telnet adaptater for Dell PowerConnect 3424 switches, but you can build
your own adatptater for your own switch model too using the `TelnetAdaptater` API defined in the
`ethernet-auth.telnet.adaptaters` module.

### Server-side switch configuration

#### Configure a new switch

In order to add a new managed switch to the platform, one entry for describing the switch should be created in the
administration of the platform under the `Switch` model.
The `name` field of this entry will be used to locate the switch configuration written in the server configuration.

Here is how a switch configuration can be declared:

```
>>> SWITCHES = {
>>>     'my-switch-1': {
>>>         'adaptater_name': 'MySwitchAdaptater',
>>>         'adaptater_module': 'path.to.my.adaptater',
>>>         'username': 'myusername',
>>>         'password': 'mypassword'
>>>     }
>>> }
```

The server has to be restarted when the configuration is updated.

#### Set-up a cron job to synchronize the managed switches

In order for the platform to update the switches configuration regularly, it is adviced to add a cron job to the user
running the project with the provided script `misc/update-switches.sh`.

Here is one example of a cron-job for switches synchronization:

```30 * * * * <path-to-the-project>/misc/./update-switches.sh```
