# JOB-SEEKING ASSISTANCE PORTAL BASED ON USER RESUME

Many job opportunities go unseen by job seekers due to the overwhelming volume of job postings daily, many of which may not align with their specific skills and career aspirations. This also poses a challenge for recruiters, who need help attracting suitable applicants for their open positions, as their job postings do not effectively reach the intended audience. Consequently, this mismatch leads to an inefficient allocation of company resources and an unnecessary expenditure of time for both employers and job seekers. Searching for job opportunities that are tailored to an individual's professional profile becomes an intensive task. Hence, we propose this portal which is a resume-based job ranking system which provides job-seeking assistance.

## Introduction
In today's job market, the vast number of daily job postings can overwhelm job seekers, leading to inefficiencies in matching skills and career goals with available opportunities. This challenge also extends to recruiters who struggle to attract suitable applicants for their open positions. To address these issues, we propose a resume-based job ranking system designed to streamline the job search process for both job seekers and recruiters.

## How to Run:

Either clone or download the repository, and then run the following commands in the terminal from the base folder:

### To run the Front-end:

bash
npm install


Start the server and Front-end:

bash
npm start 


It runs the app in the development mode.
Open http://localhost:3000 to view it in your browser.

### To run Back-end:

Open another terminal and type commands from the base folder: 

bash
cd baseline/backend/jobfinder


Install dependencies:

bash
pip install -r requirements.txt


Run backend server:

bash
python manage.py runserver


You can now run the application on the browser.

## Conclusion
In conclusion, our proposed solution portal aims to address the challenges faced by both job seekers and recruiters in the contemporary job market, mainly the IT tech industry. The sheer volume of job postings online, coupled with the complexities of job matching and recruitment processes, necessitates innovative solutions to streamline the job search experience and enhance recruitment effectiveness. 

## Future Scope
The development of our resume-based job ranking system lays a solid foundation for future enhancements and expansions. 

## Database
Our database serves as a comprehensive repository for job data scraped from Naukri.com on a weekly basis. 

## Code
The Algorithms that we are using for enabling this pipeline are mainly similarity-matching algorithms along without token weighting logic.
