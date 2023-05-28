from job import Job
from typing import Union
from requirement import Requirement


class JobIterator:

    def __init__(self, jobs: Union[list[Job], Job, None]):
        if jobs:
            if isinstance(jobs, list):
                self.jobs = jobs
            else:
                self.jobs = [jobs]
        else:
            self.jobs = []
        self.requirements = {}

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
    def common_keywords(self):
        # Returns a list of strings from a phrase formatted:
        # 'Python Pandas Testing' -> ['Python', 'Python Pandas', 'Python Pandas Testing']
        def expand_single_requirement(requirement: str, subrequirement: str,
                                      requirement_has_been_processed: bool) -> list:
            split_requirement = requirement.split()
            expanded_requirement = []
            if not requirement_has_been_processed:
                for index in range(0, len(split_requirement)):
                    expanded_requirement.append(' '.join(split_requirement[0:index + 1]))

            combined_requirements = split_requirement.copy()
            combined_requirements.extend(subrequirement.split())

            start = len(split_requirement) + 1
            stop = len(combined_requirements) + 1
            for i in range(start, stop):
                expanded_requirement.append(' '.join(combined_requirements[0:i]))
            return expanded_requirement

        def requirement_has_subrequirements(subrequirements):
            return len(subrequirements) > 0

        # Requirement and subrequirements management
        def expand_requirement(requirement: str, subrequirements: list):
            expanded_requirements = []
            if requirement_has_subrequirements(subrequirements):
                requirement_has_been_processed = False
                for i, subrequirement in enumerate(subrequirements):
                    if i > 0:
                        requirement_has_been_processed = True
                    expanded_requirement = expand_single_requirement(requirement, subrequirement,
                                                                      requirement_has_been_processed)
                    expanded_requirements.append(expanded_requirement)

            else:
                split_requirement = expand_single_requirement(requirement, subrequirement='',
                                                              requirement_has_been_processed=False)
                expanded_requirements.append(split_requirement)

            return expanded_requirements

        # Main function begins here
        if len(self.jobs) > 0:
            for job in self.jobs:
                agg_expanded_requirements = []
                for primary_requirement in job.job_requirements.keys():
                    expanded_requirements = expand_requirement(primary_requirement,
                                                          job.job_requirements[primary_requirement])
                    for expanded_requirement in expanded_requirements:
                        agg_expanded_requirements.append(expanded_requirement)
                for expanded_job_requirement in agg_expanded_requirements:
                    iteration_index = -1
                    for requirement in expanded_job_requirement:
                        processed = False
                        for processed_requirement in self.requirements:
                            if requirement == processed_requirement:
                                self.requirements[requirement].increment_count()
                                processed = True
                            elif processed_requirement in requirement:
                                if self.requirements[processed_requirement].process_as_subrequirement(requirement):
                                    processed = True
                        if not processed:
                            self.requirements[requirement] = Requirement(requirement=requirement)
        for requirement in self.requirements.values():
            requirement.print_requirements(iterations=0)
