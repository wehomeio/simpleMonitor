# Simple Monitoring
```
              _
__      _____| |__   ___  _ __ ___   ___
\ \ /\ / / _ \ '_ \ / _ \| '_ ` _ \ / _ \
 \ V  V /  __/ | | | (_) | | | | | |  __/
  \_/\_/ \___|_| |_|\___/|_| |_| |_|\___|
```
Monitoring db data changes and send to webhooks

## Usage
```
python main.py
```
or run as `daemon`
```
python main.py -d
```
or run as a one-off (no scheduling)
```
python main.py -i
``` 

## Configure
copy `config.yml.sample` to `config.yml`

`sql_config` is an array, in case there are multiple db to back up

`dry_run` do not upload to s3 if set to `True`
