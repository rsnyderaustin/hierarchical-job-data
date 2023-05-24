from job import Job
import csv

csv_file = 'jobs_and_networking.csv'

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    column_name_row=next(csv_reader)
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


