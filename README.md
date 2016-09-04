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
