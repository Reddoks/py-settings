## Little python settings management module

Inspired by need to constantly fix development code artefacts when deploy applications in docker containers.

### Features:
- Variables schema definition with default values
- JSON file creation with first run variable values
- JSON file and default values override by environment variables defined

### How to use:
You can import module and initialize setting class instance. If you set config filename - module will try to read config file in APP_WORK_DIR or create it.

``` python
from settings import Settings

config = Settings("config.json")

print(config.APP_WORK_DIR)
```

### Defaults:
First, you have to define your apps variables in two dictionaries - `defaults` (variables schema and default values) and `drop_list` (variables to be excluded from JSON file, for example - secrets).

>**Note:**
>By default, module using  APP_WORK_DIR variable to determine folder/directory to read and save JSON file. If this variable not defined,script will try to use running directory as base path.

``` json
defaults = {  
    "APP_WORK_DIR": "",
    "FLASK_HOST": "0.0.0.0",
    "FLASK_PORT": 80,
    "FLASK_SECRET": uuid.uuid4().hex,  
    "APP_VARIABLE": "Value"
}  
drop_list = [  
 "APP_WORK_DIR",  
 "APP_SECRET"  
]
```
### Usage:

``` python
app = Flask(__name__)  
app.secret_key = config.FLASK_SECRET
```
If you need to check variable exist:

```python
if "FLASK_SECRET" in settings.__dict__:
```


### Overrides:

- JSON file definitions will override default values if exist. You can set additional variables or override default with it.
- Environment variables will override both - default and JSON values, but only in case when defined in these sources.

### Config file update:
You can use `load_config` and `save_config` methods to reload and update config file. 
