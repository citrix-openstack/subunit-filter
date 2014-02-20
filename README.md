To create a subunit test stream:

    python -m subunit.run discover -t ./

This will produce a subunit stream. Now pipe it to the filter:

    python -m subunit.run discover -t ./ | python sufilter.py EXCL_LIST LOGFILE

Where `EXCL_LIST` is a text file containing unwanted test ids, one per line,
`LOGFILE` is a file that will be used to log the actions.