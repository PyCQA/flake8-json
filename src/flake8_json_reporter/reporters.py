"""Module containing all of the JSON reporters for Flake8."""
from __future__ import print_function, unicode_literals

import json

from flake8.formatting import base


class DefaultJSON(base.BaseFormatter):
    """The non-pretty-printing JSON formatter."""

    def after_init(self):
        """Force newline to be empty."""
        self.newline = ''

    def _write(self, output):
        if self.output_fd is not None:
            self.output_fd.write(output + self.newline)
        if self.output_fd is None or self.options.tee:
            print(output, end=self.newline)

    def write_line(self, line):
        """Override write for convenience."""
        self.write(line, None)

    def start(self):
        """Override the default to start printing JSON."""
        super(DefaultJSON, self).start()
        self.write_line('{')
        self.files_reported_count = 0

    def stop(self):
        """Override the default to finish printing JSON."""
        self.write_line('}')

    def beginning(self, filename):
        """We're starting a new file."""
        json_filename = json.dumps(filename)
        if self.files_reported_count > 0:
            self.write_line(', {}: ['.format(json_filename))
        else:
            self.write_line('{}: ['.format(json_filename))
        self.reported_errors_count = 0

    def finished(self, filename):
        """We've finished processing a file."""
        self.files_reported_count += 1
        self.write_line(']')

    def dictionary_from(self, violation):
        """Convert a Violation to a dictionary."""
        return {
            key: getattr(violation, key)
            for key in [
                'code',
                'filename',
                'line_number',
                'column_number',
                'text',
                'physical_line',
            ]
        }

    def format(self, violation):
        """Format a violation."""
        formatted = json.dumps(self.dictionary_from(violation))
        if self.reported_errors_count > 0:
            self.write_line(', {}'.format(formatted))
        else:
            self.write_line(formatted)
        self.reported_errors_count += 1
