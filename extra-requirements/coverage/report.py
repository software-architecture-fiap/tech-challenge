# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Summary reporting"""

from __future__ import annotations

import sys

from typing import Any, IO, Iterable, TYPE_CHECKING

from coverage.exceptions import ConfigError, NoDataError
from coverage.misc import human_sorted_items
from coverage.plugin import FileReporter
from coverage.report_core import get_analysis_to_report
from coverage.results import Analysis, Numbers
from coverage.types import TMorf

if TYPE_CHECKING:
    from coverage import Coverage


class SummaryReporter:
    """A reporter for writing the summary report."""

    def __init__(self, coverage: Coverage) -> None:
        self.coverage = coverage
        self.config = self.coverage.config
        self.branches = coverage.get_data().has_arcs()
        self.outfile: IO[str] | None = None
        self.output_format = self.config.format or "text"
        if self.output_format not in {"text", "markdown", "total"}:
            raise ConfigError(f"Unknown report format choice: {self.output_format!r}")
        self.fr_analysis: list[tuple[FileReporter, Analysis]] = []
        self.skipped_count = 0
        self.empty_count = 0
        self.total = Numbers(precision=self.config.precision)

    def write(self, line: str) -> None:
        """Write a line to the output, adding a newline."""
        assert self.outfile is not None
        self.outfile.write(line.rstrip())
        self.outfile.write("\n")

    def write_items(self, items: Iterable[str]) -> None:
        """Write a list of strings, joined together."""
        self.write("".join(items))

    def _report_text(
        self,
        header: list[str],
        lines_values: list[list[Any]],
        total_line: list[Any],
        end_lines: list[str],
    ) -> None:
        """Internal method that prints report data in text format.

        `header` is a list with captions.
        `lines_values` is list of lists of sortable values.
        `total_line` is a list with values of the total line.
        `end_lines` is a list of ending lines with information about skipped files.

        """
        # Prepare the formatting strings, header, and column sorting.
        max_name = max([len(line[0]) for line in lines_values] + [5]) + 1
        max_n = max(len(total_line[header.index("Cover")]) + 2, len(" Cover")) + 1
        max_n = max([max_n] + [len(line[header.index("Cover")]) + 2 for line in lines_values])
        formats = dict(
            Name="{:{name_len}}",
            Stmts="{:>7}",
            Miss="{:>7}",
            Branch="{:>7}",
            BrPart="{:>7}",
            Cover="{:>{n}}",
            Missing="{:>10}",
        )
        header_items = [
            formats[item].format(item, name_len=max_name, n=max_n)
            for item in header
        ]
        header_str = "".join(header_items)
        rule = "-" * len(header_str)

        # Write the header
        self.write(header_str)
        self.write(rule)

        formats.update(dict(Cover="{:>{n}}%"), Missing="   {:9}")
        for values in lines_values:
            # build string with line values
            line_items = [
                formats[item].format(str(value),
                name_len=max_name, n=max_n-1) for item, value in zip(header, values)
            ]
            self.write_items(line_items)

        # Write a TOTAL line
        if lines_values:
            self.write(rule)

        line_items = [
            formats[item].format(str(value),
            name_len=max_name, n=max_n-1) for item, value in zip(header, total_line)
        ]
        self.write_items(line_items)

        for end_line in end_lines:
            self.write(end_line)

    def _report_markdown(
        self,
        header: list[str],
        lines_values: list[list[Any]],
        total_line: list[Any],
        end_lines: list[str],
    ) -> None:
        """Internal method that prints report data in markdown format.

        `header` is a list with captions.
        `lines_values` is a sorted list of lists containing coverage information.
        `total_line` is a list with values of the total line.
        `end_lines` is a list of ending lines with information about skipped files.

        """
        # Prepare the formatting strings, header, and column sorting.
        max_name = max((len(line[0].replace("_", "\\_")) for line in lines_values), default=0)
        max_name = max(max_name, len("**TOTAL**")) + 1
        formats = dict(
            Name="| {:{name_len}}|",
            Stmts="{:>9} |",
            Miss="{:>9} |",
            Branch="{:>9} |",
            BrPart="{:>9} |",
            Cover="{:>{n}} |",
            Missing="{:>10} |",
        )
        max_n = max(len(total_line[header.index("Cover")]) + 6, len(" Cover "))
        header_items = [formats[item].format(item, name_len=max_name, n=max_n) for item in header]
        header_str = "".join(header_items)
        rule_str = "|" + " ".join(["- |".rjust(len(header_items[0])-1, "-")] +
            ["-: |".rjust(len(item)-1, "-") for item in header_items[1:]],
        )

        # Write the header
        self.write(header_str)
        self.write(rule_str)

        for values in lines_values:
            # build string with line values
            formats.update(dict(Cover="{:>{n}}% |"))
            line_items = [
                formats[item].format(str(value).replace("_", "\\_"), name_len=max_name, n=max_n-1)
                for item, value in zip(header, values)
            ]
            self.write_items(line_items)

        # Write the TOTAL line
        formats.update(dict(Name="|{:>{name_len}} |", Cover="{:>{n}} |"))
        total_line_items: list[str] = []
        for item, value in zip(header, total_line):
            if value == "":
                insert = value
            elif item == "Cover":
                insert = f" **{value}%**"
            else:
                insert = f" **{value}**"
            total_line_items += formats[item].format(insert, name_len=max_name, n=max_n)
        self.write_items(total_line_items)
        for end_line in end_lines:
            self.write(end_line)

    def report(self, morfs: Iterable[TMorf] | None, outfile: IO[str] | None = None) -> float:
        """Writes a report summarizing coverage statistics per module.

        `outfile` is a text-mode file object to write the summary to.

        """
        self.outfile = outfile or sys.stdout

        self.coverage.get_data().set_query_contexts(self.config.report_contexts)
        for fr, analysis in get_analysis_to_report(self.coverage, morfs):
            self.report_one_file(fr, analysis)

        if not self.total.n_files and not self.skipped_count:
            raise NoDataError("No data to report.")

        if self.output_format == "total":
            self.write(self.total.pc_covered_str)
        else:
            self.tabular_report()

        return self.total.pc_covered

    def tabular_report(self) -> None:
        """Writes tabular report formats."""
        # Prepare the header line and column sorting.
        header = ["Name", "Stmts", "Miss"]
        if self.branches:
            header += ["Branch", "BrPart"]
        header += ["Cover"]
        if self.config.show_missing:
            header += ["Missing"]

        column_order = dict(name=0, stmts=1, miss=2, cover=-1)
        if self.branches:
            column_order.update(dict(branch=3, brpart=4))

        # `lines_values` is list of lists of sortable values.
        lines_values = []

        for (fr, analysis) in self.fr_analysis:
            nums = analysis.numbers

            args = [fr.relative_filename(), nums.n_statements, nums.n_missing]
            if self.branches:
                args += [nums.n_branches, nums.n_partial_branches]
            args += [nums.pc_covered_str]
            if self.config.show_missing:
                args += [analysis.missing_formatted(branches=True)]
            args += [nums.pc_covered]
            lines_values.append(args)

        # Line sorting.
        sort_option = (self.config.sort or "name").lower()
        reverse = False
        if sort_option[0] == "-":
            reverse = True
            sort_option = sort_option[1:]
        elif sort_option[0] == "+":
            sort_option = sort_option[1:]
        sort_idx = column_order.get(sort_option)
        if sort_idx is None:
            raise ConfigError(f"Invalid sorting option: {self.config.sort!r}")
        if sort_option == "name":
            lines_values = human_sorted_items(lines_values, reverse=reverse)
        else:
            lines_values.sort(
                key=lambda line: (line[sort_idx], line[0]),
                reverse=reverse,
            )

        # Calculate total if we had at least one file.
        total_line = ["TOTAL", self.total.n_statements, self.total.n_missing]
        if self.branches:
            total_line += [self.total.n_branches, self.total.n_partial_branches]
        total_line += [self.total.pc_covered_str]
        if self.config.show_missing:
            total_line += [""]

        # Create other final lines.
        end_lines = []
        if self.config.skip_covered and self.skipped_count:
            file_suffix = "s" if self.skipped_count>1 else ""
            end_lines.append(
                f"\n{self.skipped_count} file{file_suffix} skipped due to complete coverage.",
            )
        if self.config.skip_empty and self.empty_count:
            file_suffix = "s" if self.empty_count > 1 else ""
            end_lines.append(f"\n{self.empty_count} empty file{file_suffix} skipped.")

        if self.output_format == "markdown":
            formatter = self._report_markdown
        else:
            formatter = self._report_text
        formatter(header, lines_values, total_line, end_lines)

    def report_one_file(self, fr: FileReporter, analysis: Analysis) -> None:
        """Report on just one file, the callback from report()."""
        nums = analysis.numbers
        self.total += nums

        no_missing_lines = (nums.n_missing == 0)
        no_missing_branches = (nums.n_partial_branches == 0)
        if self.config.skip_covered and no_missing_lines and no_missing_branches:
            # Don't report on 100% files.
            self.skipped_count += 1
        elif self.config.skip_empty and nums.n_statements == 0:
            # Don't report on empty files.
            self.empty_count += 1
        else:
            self.fr_analysis.append((fr, analysis))
