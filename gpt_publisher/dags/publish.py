import pendulum
import datetime
import random
import re

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.operators.bash import BashOperator

import openai

from gpt_publisher.constants import GPT_TOPICS, DATE_TIME_REGEX, TAGS_REGEX, gpt_prompt


with DAG(
    dag_id="publish_blog_post",
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

    @task(task_id="pick_topic")
    def pick_topic():
        length = len(GPT_TOPICS)
        index = random.randint(0, length - 1)
        return GPT_TOPICS[index]

    @task(task_id="call_gpt")
    def call_gpt(ti=None):
        """
        Calls ChatGPT 4 to generate a blog post
        """
        theme = ti.xcom_pull(task_ids="pick_topic")
        assert theme is not None or theme is not ""
        print(f"Theme: {theme}")
        prompt = gpt_prompt(theme)
        openai_api_key = Variable.get("OPENAI_API_KEY")

        openai.api_key = openai_api_key
        # response = openai.ChatCompletion.create(
        #     model="gpt-4", messages=[{"role": "user", "content": prompt}]
        # )
        # print(f"response: {response}")
        # raw_text = response["choices"][0]["message"]["content"]
        raw_text = "---\ntitle: \"Beyond Basics: Delving into the Depths of Modern Frontend Development\"\ndate: 2022-11-30\nhero:\n  preview: images/blog-preview.jpg\n  desktop: images/blog-desktop.jpg\n  tablet: images/blog-tablet.jpg\n  mobile: images/blog-mobile.jpg\n  fallback: images/blog-fallback.jpg\ntags: frontend_development, JavaScript, VueJs, ReactJs, AngularJs, NuxtJs, NextJs, PWA, WebPack, Babel\nexcerpt: \"In this blog, we will navigate the uncharted seas of advanced frontend development techniques, working with popular libraries and frameworks and working around common pitfalls and bottlenecks. Brace yourself for a journey to the \u2018beyond\u2019 of frontend development.\"\ntimeToRead: 10\nauthors:\n  - Mohseen Mukaddam\n---\n\nThe world of frontend development has taken enormous strides  in the recent years, from baking simple web pages with HTML and CSS to constructing complex single-page applications (SPAs) with modern libraries and frameworks.\n\nUnderstanding these modern technologies not only segregates ordinary frontend developers from the truly proficient ones, but it also enables one\u2019s ability to build more efficient, future-proof and maintainable applications.\n\nLet\u2019s dive in.\n\n## React, Angular, Vue - Choose Your Shield\n\nIn the battlefront of frontend development, you need a trustworthy shield. The most popular choices are React, Angular, and Vue. All three provide advanced features out of the box. However, choosing the one right for you depends on your use case. Understanding their strengths, weaknesses, and ideal use-cases is crucial.\n\n> \u201cAny application that can be written in JavaScript, will eventually be written in JavaScript.\u201d \u2013 Jeff Atwood.\n\nReact\u2019s strength lies in its flexibility and immense community support. It is backed by Facebook and its one-direction data flow is renowned. Here is a small sample of a React component:\n\n```javascript\nimport React from 'react';\n\nconst HelloWorld = () => {\n  return <p>Hello, world!</p>\n}\n\nexport default HelloWorld;\n```\nThis is arguably the most simple a React component can get. But the true power of React is realised when you need to manage state, handle user inputs and compose components. You can find many examples and resources [here](https://github.com/facebook/react).\n\nAngular, maintained by Google, is a full-fledged MVC framework rather than a lib like React or Vue, and provides much more straight out of the box. It automates two-way data binding, dependency injection and more, making it the right tool for larger scale applications.\n\nVue, on the other hand, provides the best of both Angular and React, with a lighter footprint. Here is a simple Vue component:\n\n```vue\n<template>\n  <p>{{ greeting }}</p>\n</template>\n\n<script>\nexport default {\n  data() {\n    return {\n      greeting: 'Hello, world!'\n    }\n  }\n}\n</script>\n```\nCompared to our previous React example, you can see that Vue separates the template (HTML) from the logic (JavaScript).\n\n## Building Performance-First Applications with NuxtJS and NextJS\n\nNext.js and Nuxt.js are powerful frameworks based on React and Vue respectively. These frameworks ensure better performance with features like auto code-splitting, pre-fetching, automatic routing and static site generation.\n\nIt\u2019s notable to mention the pitfalls when constructing SPAs - SEO. Often overlooked, SEO can hit you hard in the long-run as it scarifies the discoverability of your website. However, NuxtJS and NextJS are very SEO friendly.\n\nIt's vital to \"reduce, reduce, reduce. Then add lightness.\" as said by Colin Chapman. Your website needs to lose the extra pounds and pick up some speed.\n\n## WebPack and Babel\n\nJavaScript has come a long way since its inception. But with each version, the gap between modern JS (ES6/7/8) and browser-supported JS increases. Babel helps bridge this gap, converting modern JS into browser compatible JS. It's essential to any advanced frontend developer\u2019s toolkit. \n\nWebpack, on the other hand, is a module bundler. Simply put, it takes a bunch of modules, applies a series of transformations, and gives out a single (or multiple - code splitting) bundled file, optimised and ready for the browser.\n\n## Progressive Web Apps (PWAs)\n\nPWAs are the talk of the web-development town, combining the best of web and native apps. They can load when offline, receive push notifications, and even be added to a home screen. \n\nBeware, though. Although promising, PWAs are not perfect. They come with their own bag of issues including compatibility issues with iOS and the dread of managing a service worker.\n\n## Conclusion\n\nThe journey of traversing the 'beyond' of frontend development is bumpy. The terrain is hostile and pitfalls are common. However, the treasure that awaits is worth it and the view is amazing. Happy developing!\n\nRemember these wise words from Paul Graham, \"The web is the medium that rewards giving.\"\n\n---\n\nThis post barely scratches the surface of modern frontend development techniques. However, don't let that daint you. Keep exploring, keep learning; The journey is what matters after all."
        assert raw_text is not None or raw_text is not ""
        return raw_text

    @task(task_id="process_blog_post")
    def process_blog_post(ti=None):
        """
        Processes the blog post, sanitizes date and tags
        """
        post = ti.xcom_pull(task_ids="call_gpt")
        assert post is not None or post is not ""
        
        date = datetime.datetime.now().isoformat().split("T")[0]
        post = re.sub(DATE_TIME_REGEX, f"date: {date}", post)

        tags = re.findall(TAGS_REGEX, post)
        tags = tags[0].split(",")
        tags = [tag.strip() for tag in tags]
        tags = [tag.replace("_", " ").replace("-", " ") for tag in tags]

        return {
            "post": post,
            "tags": tags,
            "date": date,
        }

    @task(task_id="fetch_images")
    def fetch_images(ti=None):
        pass

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
            """,
        }

    clone_url = get_clone_link()
    blog_post = mock_blog_post()

    pick_topic = pick_topic()
    call_gpt = call_gpt()
    process_blog_post = process_blog_post()

    # run = BashOperator(
    #     task_id="publish_blog_post",
    #     bash_command="/opt/airflow/dags/scripts/publish.sh ",
    #     env={
    #         "CLONE_URL": clone_url,
    #         "BLOG_FILENAME": f"{blog_post['title']}.md",
    #         "BLOG_CONTENT": blog_post["body"],
    #     },
    # )

    end = BashOperator(
        task_id="end",
        bash_command='echo "Shutting down!"',
    )

    pick_topic >> call_gpt >> process_blog_post >> end

if __name__ == "__main__":
    dag.test()
