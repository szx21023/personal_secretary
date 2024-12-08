# from main import app

# class BaseJob:
#     name = 'default'
    
#     func = None
#     run_date = None
#     job_id = None
#     args = []

#     def __init__(self, run_date, _id, args): # args need to be changed
#         self.run_date = run_date
#         self.job_id = f"{self.name}_{_id}"
#         self.args = args
        
#     def start(self):
#         print(f"setup scheduler_job, name: {self.name}, job_id: {self.job_id}, run_date: {self.run_date}")
#         job = app.scheduler.add_job(
#             app.job.get(self.name).func, 'date', run_date=self.run_date, id=self.job_id, args=self.args
#         )