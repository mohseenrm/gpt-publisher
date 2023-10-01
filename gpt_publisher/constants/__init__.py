GPT_TOPICS = [
    "Advanced Typescript Tutorial",
    "Advanced Web development tutorial",
    "Advanced Full stack development",
    "Advanced Frontend Development",
    "Functional Programming",
    "Performant NodeJS Tutorial",
    "Performant and responsive UI tutorial",
    "Advanced redux tutorial",
    "Anti-patterns in Typescript",
    "Advanced docker tutorial",
    "Advanced Bash scripting tutorial",
    "Best CLI tools",
    "Profiling in React tutorial",
    "Profiling in NodeJS tutorial",
]


def gpt_prompt(theme: str) -> str:
    return f"""
You are an influential software developer blogger. Write a 7-15 min long SEO-friendly blog post in markdown format with the given template and these requirements:

1. The theme is "{theme}"
2. The blog post should cover this theme without directly referencing the chosen theme.
3. Should have tags relevant to the blog post
4. Should contain code examples
5. Use public Github code examples where possible
6. Use quotes when appropriate
7. Use references from different authors
8. Dive into different modern techniques
9. Explain different gotchas and pitfalls

Template:
---
title: "<BLOG_POST_TITLE>"
date: <TIMESTAMP_NOW>
hero:
  preview:
  desktop:
  tablet:
  mobile:
  fallback:
tags: <RELEVANT_TAGS>
excerpt: "<BLOG_POST_EXCERPT>"
timeToRead: <TIME_TO_READ>
authors:
  - Mohseen Mukaddam
---

<BLOG_POST_CONTENT>
    """
