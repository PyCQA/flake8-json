"""Module containing all of the JSON reporters for Flake8."""
import hashlib
import json
import textwrap

from flake8.formatting import base


class DefaultJSON(base.BaseFormatter):
    """The non-pretty-printing JSON formatter."""

    def after_init(self):
        """Force newline to be empty."""
        self.newline = ""

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
        super().start()
        self.write_line("{")
        self.files_reported_count = 0

    def stop(self):
        """Override the default to finish printing JSON."""
        self.write_line("}")

    def beginning(self, filename):
        """We're starting a new file."""
        json_filename = json.dumps(filename)
        if self.files_reported_count > 0:
            self.write_line(f", {json_filename}: [")
        else:
            self.write_line(f"{json_filename}: [")
        self.reported_errors_count = 0

    def finished(self, filename):
        """We've finished processing a file."""
        self.files_reported_count += 1
        self.write_line("]")

    def dictionary_from(self, violation):
        """Convert a Violation to a dictionary."""
        return {
            key: getattr(violation, key)
            for key in [
                "code",
                "filename",
                "line_number",
                "column_number",
                "text",
                "physical_line",
            ]
        }

    def format(self, violation):
        """Format a violation."""
        formatted = json.dumps(self.dictionary_from(violation))
        if self.reported_errors_count > 0:
            self.write_line(f", {formatted}")
        else:
            self.write_line(formatted)
        self.reported_errors_count += 1


def _indent(text, indent):
    return textwrap.indent(text, " " * indent)


class FormattedJSON(DefaultJSON):
    """Pretty-printing JSON formatter."""

    def stop(self):
        """Override the default to finish printing JSON."""
        if self.files_reported_count > 0:
            self.write_line("\n")
        self.write_line("}\n")

    def beginning(self, filename):
        """We're starting a new file."""
        if self.files_reported_count > 0:
            self.write_line(",\n")
            self.write_line(f"  {json.dumps(filename)}: [")
        else:
            self.write_line(f"\n  {json.dumps(filename)}: [")
        self.reported_errors_count = 0

    def finished(self, filename):
        """We've finished processing a file."""
        self.files_reported_count += 1
        if self.reported_errors_count > 0:
            self.write_line("\n")
            self.write_line("  ]")
        else:
            self.write_line("]")

    def format(self, violation):
        """Format a violation."""
        formatted = json.dumps(self.dictionary_from(violation), indent=2)
        formatted = _indent(formatted, indent=4)
        if self.reported_errors_count > 0:
            self.write_line(",")
        self.write_line("\n")
        self.write_line(formatted)
        self.reported_errors_count += 1


class CodeClimateJSON(base.BaseFormatter):
    """Formatter for CodeClimate JSON."""

    def after_init(self):
        """Force newline to be empty."""
        self.newline = ""

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
        super().start()
        self.write_line("{")
        self.files_reported_count = 0

    def stop(self):
        """Override the default to finish printing JSON."""
        self.write_line("}")

    def beginning(self, filename):
        """We're starting a new file."""
        json_filename = json.dumps(filename)
        if self.files_reported_count > 0:
            self.write_line(f", {json_filename}: [")
        else:
            self.write_line(f"{json_filename}: [")
        self.reported_errors_count = 0

    def finished(self, filename):
        """We've finished processing a file."""
        self.files_reported_count += 1
        self.write_line("]")

    @staticmethod
    def _fingerprint(violation):
        return hashlib.md5(
            "{}:{}:{}:{}".format(
                violation.filename,
                violation.code,
                violation.line_number,
                violation.physical_line,
            ).encode()
        ).hexdigest()

    def dictionary_from(self, violation):
        """Convert a Violation to a dictionary."""
        # https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#data-types
        return {
            "type": "issue",
            "check_name": violation.code,
            "description": violation.text,
            "categories": ["Style"],  # TODO: guess based on well-known codes?
            "severity": "minor",
            "location": {
                "path": violation.filename,
                "positions": {
                    "begin": {
                        "line": violation.line_number,
                        "column": violation.column_number,
                    },
                    "end": {
                        "line": violation.line_number,
                        "column": violation.column_number,
                    },
                },
            },
            "fingerprint": self._fingerprint(violation),
        }

    def format(self, violation):
        """Format a violation."""
        formatted = json.dumps(self.dictionary_from(violation))
        if self.reported_errors_count > 0:
            self.write_line(f", {formatted}")
        else:
            self.write_line(formatted)
        self.reported_errors_count += 1
