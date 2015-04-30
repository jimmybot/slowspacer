# slowspacer
When tailing logs, add some space to easily differentiate between stale and current logs

Ever try to debug something by watching a log and get confused about which log lines were new
and which were stale and already there?  Pipe your tail to slowspacer and after receiving no logs
for N seconds (default is 3), it will add space and a marker to create visual separation between
batches of logs.

TODO: This depends on Python, and it would be nice to rewrite it in C or Rust so it didn't.

Example: tail -f /var/log/yourlog.log | slowspacer
Output:

    [1430428323] batch 1 log line 1
    [1430428323] batch 1 log line 2
    [1430428323] batch 1 log line 3
    
    ================================================================================
    
    [1430428327] batch 2 log line 1
    [1430428327] batch 2 log line 2
    [1430428327] batch 2 log line 3
