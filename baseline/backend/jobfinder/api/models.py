from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=200, unique=True)
    company_id = models.CharField(max_length=200, null=True, blank=True)
    jd_url = models.CharField(max_length=500)
    skills = models.TextField(null=True, blank=True)
    job_description = models.TextField()
    extra_data = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=1000)
    company_name = models.CharField(max_length=500)
    posted_on = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=100)

    def __str__(self):
        return self.title