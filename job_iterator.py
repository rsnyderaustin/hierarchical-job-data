from job import Job
from typing import Union
from collections import namedtuple

class JobIterator:

    def __init__(self, jobs: Union[list[Job], Job, None]):
        if jobs:
            if isinstance(jobs, list):
                self.jobs = jobs
            else:
                self.jobs = [jobs]
        else:
            self.jobs = []

    # Returns a dict {job_company, job_title): requirement: [sub_requirements]}
    def combine_requirements(self) -> dict[tuple:list]:
        combined_requirements_dict = {}
        for job in self.jobs:
            job_key = (job.job_company, job.job_title)
            combined_requirements_dict[job_key] = []
            for job_requirement in job.job_requirements:
                if job.job_requirements[job_requirement]:
                    for sub_requirement in job.job_requirements[job_requirement]:
                        combined_requirements_dict[job_key].append(f"{job_requirement} {sub_requirement}")
                else:
                    combined_requirements_dict[job_key].append(f"{job_requirement}")
        return combined_requirements_dict

    # Iterates through each job and its requirements, tallying keywords in a dict
    # Keywords are analyzed based on each term from the base term
    # "Azure SQL Data Warehousing" -> "Azure", "Azure SQL", "Azure SQL Data", "Azure SQL Data Warehousing"
    # {requirement: [subrequirements]
    def common_keywords(self) -> dict:
        RequirementCount = namedtuple('RequirementCount', ('requirement', 'count'))
        keywords_tally: dict[RequirementCount, list[RequirementCount]] = {}
        if len(self.jobs) > 0:
            for job in self.jobs:
                for requirement in job.job_requirements:
                    print(f"Working on {job.job_title} at {job.job_company} requirement: {requirement}")
                    if requirement in keywords_tally:
                        keywords_tally[requirement].count += 1
                    else:
                        keywords_tally[requirement] = RequirementCount(requirement, 1)
                    if len(job.job_requirements[requirement]) > 0:
                        for subrequirement in job.job_requirements[requirement]:
                            if subrequirement in keywords_tally[requirement]:
                                keywords_tally[requirement][subrequirement].count += 1
                            else:
                                keywords_tally[requirement] = [RequirementCount(f"{requirement} {subrequirement}", 1)]

        return keywords_tally

