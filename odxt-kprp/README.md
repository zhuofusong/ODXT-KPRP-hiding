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

__Repeat the same set of commands as above to generate test data and experiment logs in the root folder of ODXT (and HDXT) project for comparison. Change the name of logs to "test/result_server_odxt.log" and "test/result_client_odxt.log". Copy the logs generated into the test folder for ploting figures__

## Plot the figures
In the current folder, run
```sh
python test/result_plot.py
```
This will generate figures reported in the experiment section of the paper.