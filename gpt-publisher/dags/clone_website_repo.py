import pendulum
import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="clone_repo",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["gpt-publisher"],
) as dag:
    def get_clone_link():
        token = Variable.get("GITHUB_TOKEN")
        username = Variable.get("GITHUB_USER")
        repo = Variable.get("GITHUB_REPOSITORY")
        clone_link = f"https://{username}:{token}@github.com/{repo}"
        print(f"SECRET: {token}")
        return clone_link

    def mock_blog_post():
        date = datetime.datetime.now().isoformat().split("T")[0]
        return {
            "title": f"{date}-hello-world",
            "body": """
---
title: "Preparing to be a Dog Parent"
date: 2021-12-26T12:34:37-08:00
hero:
  preview: /images/hero/preparing-to-be-a-dog-parent.jpg
  desktop: /images/hero/preparing-to-be-a-dog-parent.jpg
  tablet: /images/hero/preparing-to-be-a-dog-parent-tablet.jpg
  mobile: /images/hero/preparing-to-be-a-dog-parent-mobile.jpg
  fallback: /images/hero/preparing-to-be-a-dog-parent.jpg
excerpt: "Lessons on becoming a paw parent and how to dog proof your home."
timeToRead: 5
authors:
  - Mohseen Mukaddam
---

Hello!
            """
        }

    clone_url = get_clone_link()
    blog_post = mock_blog_post()

    run = BashOperator(
        task_id="publish_blog_post",
        bash_command="/opt/airflow/dags/scripts/publish.sh ",
        env={
            "CLONE_URL": clone_url,
            "BLOG_FILENAME": f"{blog_post['title']}.md",
            "BLOG_CONTENT": blog_post["body"],
        },
    )

    end = BashOperator(
        task_id="end",
        bash_command='echo "Shutting down!"',
    )

    run >> end


if __name__ == "__main__":
    dag.test()
