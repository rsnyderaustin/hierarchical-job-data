from typing import Union


class Job:

    def __init__(self, job_company: str, job_title: str, job_requirements: Union[dict, None]):
        '''

        :param job_company:
        :param job_title:
        :param job_requirements: A dict of job requirements with values being a list of subrequirements, if applicable
        '''
        self.job_company = job_company
        self.job_title = job_title
        if job_requirements is not None:
            self.job_requirements = job_requirements
        else:
            self.job_requirements = {}

    def add_job_requirement(self, job_requirement: str):
        self.job_requirements[job_requirement] = []

    def add_sub_requirement(self, job_requirement: str, sub_requirement: str):
        try:
            self.job_requirements[job_requirement].append(sub_requirement)
        except KeyError:
            print(f"{job_requirement} does not exist in {self.job_title} at {self.job_company}.")
