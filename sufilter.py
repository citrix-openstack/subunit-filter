import sys
import subunit
import argparse


class FilterStreamer(subunit.StreamResultToBytes):
    def __init__(self, output_stream, excluded_ids, logfile):
        super(FilterStreamer, self).__init__(output_stream)
        self.excluded_ids = excluded_ids
        self.logfile = logfile

    def should_exclude(self, test_id):
        return test_id in self.excluded_ids

    def status(self, test_id=None, test_status=None, test_tags=None,
        runnable=True, file_name=None, file_bytes=None, eof=False,
        mime_type=None, route_code=None, timestamp=None):
        if self.should_exclude(test_id):
            self.log_exclusion(test_id)
        else:
            self.log_inclusion(test_id)
            return super(FilterStreamer, self).status(
                test_id=test_id, test_status=test_status, test_tags=test_tags,
                runnable=runnable, file_name=file_name, file_bytes=file_bytes,
                eof=eof, mime_type=mime_type, route_code=route_code,
                timestamp=timestamp)

    def _log(self, status, test_id):
        self.logfile.write(status + test_id + '\n')

    def log_exclusion(self, test_id):
        self._log('EXCLUDED', test_id)

    def log_inclusion(self, test_id):
        self._log('INCLUDED', test_id)


def load_id_list(path):
    test_ids = []
    with open(path, 'rb') as list_file:
        for line in list_file.readlines():
            stripped_line = line.strip()
            if stripped_line:
                test_ids.append(stripped_line)

        list_file.close()

    return test_ids


def main():
    parser = argparse.ArgumentParser(description="Subunit filter")
    parser.add_argument("exclude")
    parser.add_argument("logfile")
    args = parser.parse_args()

    excluded_ids = load_id_list(args.exclude)

    with open(args.logfile, 'wb') as logfile:
        stream_reader = subunit.ByteStreamToStreamResult(sys.stdin)

        stream_writer = FilterStreamer(sys.stdout, excluded_ids, logfile)

        stream_writer.startTestRun()
        stream_reader.run(stream_writer)
        stream_writer.stopTestRun()


if __name__ == "__main__":
    main()





