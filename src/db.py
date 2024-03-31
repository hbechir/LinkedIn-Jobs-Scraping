import json
import mysql.connector

def insert_data(db, data):
    cursor = db.cursor()

    for job_group in data:
        job_title = job_group['jobtitle']
        for job in job_group['jobs']:
            # Check if job title exists
            cursor.execute("SELECT * FROM job_title WHERE job_title = %s", (job_title,))
            if cursor.fetchone() is None:
                # If job title doesn't exist, insert it
                cursor.execute("INSERT INTO job_title (job_title) VALUES (%s)", (job_title,))

            # Get job title id
            cursor.execute("SELECT id FROM job_title WHERE job_title = %s", (job_title,))
            title_id = cursor.fetchone()[0]

            # Check if company exists
            cursor.execute("SELECT * FROM company WHERE name = %s", (job['company'],))
            if cursor.fetchone() is None:
                # If company doesn't exist, insert it
                cursor.execute("INSERT INTO company (name) VALUES (%s)", (job['company'],))

            # Get company id
            cursor.execute("SELECT id FROM company WHERE name = %s", (job['company'],))
            company_id = cursor.fetchone()[0]

            # Insert job data
            cursor.execute("INSERT INTO job (job_name, title_id, company_id, location, applicants, job_condition, time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (job['title'], title_id, company_id, job['location'], job['applicants'], job['condition'], job['time']))

            # Get job id
            cursor.execute("SELECT LAST_INSERT_ID()")
            job_id = cursor.fetchone()[0]

            for skill in job['skills']:
                # Check if skill exists
                cursor.execute("SELECT * FROM skills WHERE name = %s", (skill,))
                if cursor.fetchone() is None:
                    # If skill doesn't exist, insert it
                    cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill,))

                # Get skill id
                cursor.execute("SELECT id FROM skills WHERE name = %s", (skill,))
                skill_id = cursor.fetchone()[0]

                # Insert into job_skills
                cursor.execute("INSERT INTO job_skills (job_id, skill_id) VALUES (%s, %s)", (job_id, skill_id))

    # Commit changes
    db.commit()

    cursor.close()

def main():
    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="linkedin_webscraping1"
    )

    # Load data from JSON file
    with open('jobs.json') as f:
        data = json.load(f)

    # Insert data into database
    insert_data(db, data)

    db.close()

if __name__ == "__main__":
    main()