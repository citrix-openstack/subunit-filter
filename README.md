To create a subunit test stream:

    python -m subunit.run discover -t ./ --list

To list it for humans:

    python -m subunit.run discover -t ./ --list | subunit-ls --exists

This will produce a subunit stream. Now pipe it to the filter:

    python -m subunit.run discover -t ./ --list | python sufilter.py EXCL_LIST LOGFILE

Where `EXCL_LIST` is a text file containing unwanted test ids, one per line,
`LOGFILE` is a file that will be used to log the actions.
