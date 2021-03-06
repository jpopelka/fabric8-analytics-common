"""Code coverage page generator."""

from mako.template import Template
import os
import sys
import time
import shutil
import re

from repositories import *
from source_files import *
from unit_tests import *


class Results():
    """Class representing results gathered by the cc to be published."""

    def __init__(self):
        """Prepare empty result structure."""
        self.repositories = {}
        self.repo_prefix = "https://github.com/fabric8-analytics/"
        self.source_files = {}
        self.improvement = {}
        self.f = lambda number: '{0:.2f}'.format(number)  # function to format floating point number
        self.generated_on = time.strftime('%Y-%m-%d %H:%M:%S')
        self.unit_test_coverage = {}

    def __repr__(self):
        """Return textual representation of all results."""
        template = "Unit test coverage: {unit_test_coverage}\n"
        return template.format(unit_test_coverage=self.unit_test_coverage)


def generate_coverage_page(results):
    """Generate the code coverage HTML page with measured content."""
    template = Template(filename="template/coverage.html")
    generated_page = template.render(**results.__dict__)
    with open("coverage.html", "w") as fout:
        fout.write(generated_page)


def prepare_data_for_repositories(repositories, results):
    """Accumulate results."""
    results.repositories = repositories
    for repository in repositories:
        results.source_files[repository] = get_source_files(repository)
        results.unit_test_coverage[repository] = []
        for week in range(0, 2):
            coverage = read_unit_test_coverage_for_week(repository, week)
            print(coverage)
            results.unit_test_coverage[repository].append(coverage)
        update_improvement(results, repository)
    for repository in repositories:
        print(results.improvement[repository])


def update_improvement(results, repository):
    """Update the 'improvement' message."""
    results.improvement[repository] = ""
    try:
        week0 = float(results.unit_test_coverage[repository][0].get("coverage"))
        week1 = float(results.unit_test_coverage[repository][1].get("coverage"))
        print(week0, week1)
        if week0 == week1:
            result = "same"
        elif week0 > week1:
            result = "worse"
        else:
            result = "better"
        results.improvement[repository] = result
    except Exception as e:
        pass


def main():
    """Entry point to the CC reporter."""
    results = Results()

    prepare_data_for_repositories(repositories, results)

    generate_coverage_page(results)


if __name__ == "__main__":
    # execute only if run as a script
    main()
