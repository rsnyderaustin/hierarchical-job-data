import pytest
import csv
from job import Job
from job_iterator import JobIterator

csv_file = 'job_requirements_test.csv'


@pytest.fixture
def create_job_iterator():
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        unused_column_name_row = next(csv_reader)
        jobs = []
        job = None
        for row in csv_reader:
            if row[0] and row[1]:
                job = Job(job_company=row[0], job_title=row[1], job_requirements=None)
                jobs.append(job)
            if row[2]:
                job.add_job_requirement(row[2])
                last_requirement = row[2]
            if row[3]:
                job.add_sub_requirement(job_requirement=last_requirement, sub_requirement=row[3])
        return JobIterator(jobs)


def test_combine_requirements(create_job_iterator):
    combined_requirements = create_job_iterator._combine_requirements()
    expected_output = {
        ('Company A', 'Software Engineer'): ['Python Pandas', 'Python Testing',
                                             'Communication Presentations', 'C#'],
        ('Company B', 'Data Analyst'): ['Tableau', 'SQL'],
        ('Company C', 'Manager'): ['Communication', 'C# Testing']
    }
    assert combined_requirements == expected_output


def test_common_keywords(create_job_iterator):
    keyword_tally = create_job_iterator.common_keywords()
    expected_output = {
        'Python': {
            'count': 2,
            'Python Pandas': {
                'count': 2,
                'Python Pandas Testing': {
                    'count': 1
                }
            }
        },
        'Communication': {
            'count': 2,
            'Communication Presentations': {
                'count': 1
            }
        },
        ('C#', 2): {
            'count': 2,
            'C# Testing': {
                'count': 1
            }
            ('C# Testing', 1),
            ('C# Testing Structure', 1)
        },
        ('Tableau', 1): {},
        ('SQL', 1): {},
        ('Pandas', 1): {}
    }

    assert keyword_tally == expected_output


pytest.main()
