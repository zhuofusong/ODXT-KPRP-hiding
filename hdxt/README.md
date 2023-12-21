# ODXT-KPRP-hiding
DSSE ODXT implemetation, with KPRP-hiding property

## Generate synthetic test data

In the current folder, run
```sh
python test/test_data.py
```
[File ID list](/test/ids.txt), [keywords list](/test/keywords.txt), [updates list](/test/updates.txt) can be generated. 

## Run test

In the current folder, run
```sh
python odxt/odxt_server.py >> test/result_server.log
``` 
In a new shell, run
```sh
python odxt/odxt_client.py >> test/result_client.log
```

After tests have been executed, press Ctrl+C in the server's terminal to halt the odxt_server.py process. 