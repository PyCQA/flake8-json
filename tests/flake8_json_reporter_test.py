from argparse import Namespace

import pytest
from flake8.violation import Violation

from flake8_json_reporter.reporters import FormattedJSON


@pytest.fixture
def formatter():
    """Return a ``FormattedJSON`` instance."""
    options = Namespace(output_file=None, color=False, tee=False)
    formatter = FormattedJSON(options)
    return formatter


@pytest.fixture
def violation():
    return Violation(
        code="E222",
        filename="main.py",
        line_number=42,
        column_number=4,
        text="multiple spaces after operator",
        physical_line="x =  1",
    )


def run(formatter, violations):
    formatter.start()
    for filename in violations:
        formatter.beginning(filename)
        for violation in violations[filename]:
            formatter.format(violation)
        formatter.finished(filename)
    formatter.stop()


def test_no_files(capsys, formatter):
    run(formatter, {})
    stdout, _ = capsys.readouterr()
    assert stdout == "{}\n"


def test_single_file_no_violations(capsys, formatter):
    run(formatter, {"main.py": []})
    stdout, _ = capsys.readouterr()
    expected = """\
{
  "main.py": []
}
"""
    assert stdout == expected


def test_multiple_files_no_violations(capsys, formatter):
    run(formatter, {"main.py": [], "__init__.py": []})
    stdout, _ = capsys.readouterr()
    expected = """\
{
  "main.py": [],
  "__init__.py": []
}
"""
    assert stdout == expected


def test_single_file_single_violation(capsys, formatter, violation):
    run(formatter, {"main.py": [violation]})
    stdout, _ = capsys.readouterr()
    expected = """\
{
  "main.py": [
    {
      "code": "E222",
      "filename": "main.py",
      "line_number": 42,
      "column_number": 4,
      "text": "multiple spaces after operator",
      "physical_line": "x =  1"
    }
  ]
}
"""
    assert stdout == expected


def test_single_file_multiple_violations(capsys, formatter, violation):
    run(formatter, {"main.py": [violation] * 3})
    stdout, _ = capsys.readouterr()
    expected = """\
{
  "main.py": [
    {
      "code": "E222",
      "filename": "main.py",
      "line_number": 42,
      "column_number": 4,
      "text": "multiple spaces after operator",
      "physical_line": "x =  1"
    },
    {
      "code": "E222",
      "filename": "main.py",
      "line_number": 42,
      "column_number": 4,
      "text": "multiple spaces after operator",
      "physical_line": "x =  1"
    },
    {
      "code": "E222",
      "filename": "main.py",
      "line_number": 42,
      "column_number": 4,
      "text": "multiple spaces after operator",
      "physical_line": "x =  1"
    }
  ]
}
"""
    assert stdout == expected
