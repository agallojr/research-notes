
from qc_grader.challenges.qgss_2024 import grade_lab4_ex7, grade_lab4_ex8
from qc_grader.challenges.qgss_2024 import lab4_ex7_get_data

from qiskit.primitives import PrimitiveResult
import statistics

# Code to grab all of the expectation values
# Exercise 7: Parse all the data
all_job_data = {}

all_job_data = lab4_ex7_get_data()

#for phase in all_job_data:
#    print("****")
#    print(all_job_data[job])

#grade_lab4_ex7(all_job_data)

# Your code goes here
avg_z_data = {}
avg_z_data['Anisotropic'] = []
avg_z_data['XXX'] = []

ani = all_job_data['Anisotropic']
xxx = all_job_data['XXX']

for x in ani:
    for r in x._pub_results: 
        avg = statistics.mean(r.data.evs)
        avg_z_data['Anisotropic'].append(avg)

for x in xxx:
    for r in x._pub_results: 
        avg = statistics.mean(r.data.evs)
        avg_z_data['XXX'].append(avg)

#print(avg_z_data['Anisotropic'])
#print(avg_z_data['XXX'])

grade_lab4_ex8({'Anisotropic':avg_z_data['Anisotropic'],
                'XXX':avg_z_data['XXX']})



