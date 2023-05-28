# HierarchicalJobData

Parses through a csv file of jobs and their job requirements. Counts the number of instances that a requirement shows up among all jobs. I developed this program during my job search in order to understand more systematically what requirements were most important in the jobs I was interested in.

The program analyzes job requirement data, transforms the data into parent and subrequirement Requirement objects, then recursively analyzes the Requriements for each parent Requirement.
