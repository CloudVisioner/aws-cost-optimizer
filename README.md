# AWS Cloud Cost Optimization Tool

This is a simple Python project I built to help find unused or unnecessary AWS resources that might be quietly increasing your monthly bill.

It checks for:
- Stopped EC2 instances
- Unattached EBS volumes
- Idle RDS databases

After scanning, it estimates how much those resources might be costing and saves a basic .csv report you can easily check and act on.

---

## Why I made this

I created this tool to:
- Learn how cloud cost management works
- Practice using Python with AWS services
- Build something practical that helps reduce waste

---

## What it uses

- Python
- boto3 (AWS SDK for Python)
- csv (built-in Python module for saving reports)

No extra libraries or tools. Just a clean script doing the job.

---

## Project overview

The diagram below shows how the tool works from start to finish:

![Architecture](images/architecture.png)

---

## Future ideas

While this version runs manually, it’s built to support more features like:
- Sending the report by email
- Automatically running every week using cron or AWS Lambda

---

## Built by

Azamat Abdulazizov  
Learning cloud engineering and building real-world tools along the way
