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
        def split_requirement_phrase(requirement: str, subrequirement: str, requirement_has_been_processed: bool) -> list:
            split_requirement = requirement.split()
            expanded_requirement = []
            if not requirement_has_been_processed:
                for index in range(0, len(split_requirement)):
                    expanded_requirement.append(' '.join(split_requirement[0:index+1]))

            combined_requirements = split_requirement.copy()
            combined_requirements.extend(subrequirement.split())

            start = len(split_requirement) + 1
            stop = len(combined_requirements)
            for i in range(start, stop):
                expanded_requirement.append(' '.join(combined_requirements[0:i]))
            return expanded_requirement

        # 'Python Pandas Testing' -> ['Python', 'Python Pandas', 'Python Pandas Testing'] for each query, subquery pair
        def create_expanded_phrases(requirement: str, subrequirements: list):
            split_phrases = []
            if len(subrequirements) > 0:
                requirement_has_been_processed = False
                for i, subrequirement in enumerate(subrequirements):
                    if i > 0:
                        requirement_has_been_processed = True
                    split_requirements = split_requirement_phrase(requirement, subrequirement,
                                                                  requirement_has_been_processed)
                    split_phrases.append(split_requirements)

            else:
                # If there are no subrequirements, only analyze the requirement
                split_phrases.append(split_requirement_phrase(requirement, '', False))

            expanded_phrases = []
            for split_phrase in split_phrases:
                for i in range(len(split_phrase)):
                    for j in range(i + 1):
                        expanded_phrases.append(' '.join(split_phrase[0:j + 1]))
            return expanded_phrases
        if len(self.jobs) > 0:
            for job in self.jobs:
                new_phrases = []
                for requirement_phrase in job.job_requirements.keys():
                    new_expanded_phrase = create_expanded_phrases(requirement_phrase,
                                                                  job.job_requirements[requirement_phrase])
                    new_phrases.append(new_expanded_phrase)
                for job_phrases in new_phrases:
                    for phrase in job_phrases:
                        processed = False
                        for requirement in self.requirements.values():
                            if phrase == requirement.phrase:
                                self.requirements[phrase].increment_count()
                                processed = True
                            elif requirement.phrase in phrase:
                                requirement.check_subrequirement(phrase)
                                processed = True
                        if not processed:
                                self.requirements[phrase] = Requirement(phrase=phrase)
        for requirement in self.requirements.values():
            requirement.print_requirements()
