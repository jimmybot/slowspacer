# slowspacer
When tailing logs, add some space to easily differentiate between stale and current logs

Ever try to debug something by watching a log and get confused about which log
lines were new and which were stale and already there?  Pipe your tail to
slowspacer and after receiving no logs for N seconds (default is 3), it will
add space and a marker (default is a line of '=') to create visual separation
between batches of logs.

Known to work with both Python 2.7 and Python 3.4

TODO: This depends on Python, and it would be nice to rewrite it in C or Rust so it didn't.

Example: tail -f /var/log/yourlog.log | slowspacer

Output:

    [1430428323] batch 1 log line 1
    [1430428323] batch 1 log line 2
    [1430428324] batch 1 log line 3
    
    ================================================================================
    
    [1430428328] batch 2 log line 1
    [1430428329] batch 2 log line 2
    [1430428330] batch 2 log line 3

Instead of:

    [1430428323] batch 1 log line 1
    [1430428323] batch 1 log line 2
    [1430428324] batch 1 log line 3
    [1430428328] batch 2 log line 1
    [1430428329] batch 2 log line 2
    [1430428330] batch 2 log line 3

