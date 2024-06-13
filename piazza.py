import json
import matplotlib.pyplot as plt
from collections import defaultdict
import datetime
import pandas as pd
from piazza_api import Piazza
import getpass

#individual stats for a course
def mystats(course,display=True):
  stats = course.get_statistics()
  activity = stats['users']

  for student in activity:
    if (display):
      print("Total Contributions: " + str(student['posts']))
      print("Days Online: " + str(student['days']))
      print("Questions/Answers: " + str(student['asks']) + "/" + str(student['answers']))
      print("Posts Viewed: " + str(student['views']))
      print("-"*20)

    return [student['posts'], student['days'], student['asks'], student['answers'], student['views']]



#usage stats for a course
def activity_monitor(course):
  stats = course.get_statistics()
  activity = stats['daily']
  df = pd.DataFrame(activity)

  df['raw_day'] = pd.to_datetime(df['raw_day'], format='%Y%m%d')

  first_date = df['raw_day'].min()
  four = first_date + pd.DateOffset(months=4)

  df_filter = df[(df['raw_day'] >= first_date) & (df['raw_day'] <= four)]


  plt.figure(figsize=(10,4))


  plt.plot(df_filter['raw_day'], df_filter['users'], label='Users')
  plt.plot(df_filter['raw_day'], df_filter['posts'], label='Posts')

  plt.title('User Activity Over Time')
  plt.xlabel('Date')
  plt.ylabel('Count')

  plt.xticks(rotation=45)

  plt.legend()

  plt.tight_layout()
  plt.show()


#quick stats for a course
def glance(course):
  stats = course.get_statistics()
  info = stats['total']
  print("Total Posts: " + str(info['posts']))
  print("Instructor Answers: " + str(info['i_answers']))
  print("Student Answers: " + str(info['s_answers']))
  response_time_minutes = round(info['response_time'] / 60)
  print("Average Response Time: " + str(response_time_minutes) + " mins")
  print("-"*20)


#top ppl for a course (5)
def leaderboards(course):
  stats = course.get_statistics()
  info = stats['top_users']
  max_contributions = max(student['posts'] for student in info)
  max_days = max(student['days'] for student in info)
  max_answers = max(student['answers'] for student in info)
  max_views = max(student['views'] for student in info)
  #print(max_contributions, max_days, max_answers, max_views)



  for student in info:
    print("Name: " + str(student['name']))
    contributions = "Contributions: " + str(student['posts'])
    if (student['posts'] == max_contributions):
      contributions += " 🥇"

    print(contributions)

    days = "Days Online: " + str(student['days'])
    if (student['days'] == max_days):
      days += " 🥇"

    print(days)

    qa = "Questions/Answers: " + str(student['asks']) + "/" + str(student['answers'])

    if (student['answers'] == max_answers):
      qa += " 🥇"

    print(qa)

    posts = "Posts Viewed: " + str(student['views'])
    if (student['views'] == max_views):
      posts += " 🥇"

    print(posts)

    print("\n")

  #in order of contributions

def intro(a):
  blob = a.get_user_profile()
  name = blob['name']
  print("Hello, " + name)
  print("\n")

def course_breakdown(a):
  data = a.get_user_classes()
  grouped_courses = {}
  for course in data:
      term = course['term']
      if term not in grouped_courses:
          grouped_courses[term] = []
      grouped_courses[term].append({
          'name': course['name'],
          'num': course['num'],
          'nid': course['nid']
      })

  terms = grouped_courses.keys()
  for term in terms:
    print(term)
  sem = input("Pick a Semester: ")
  #print(grouped_courses[sem])
  return grouped_courses[sem]
  semester_breakdown(grouped_courses[sem])

def semester_breakdown(sem):
  print("Pick a Course: ")
  for course in sem:
    print(course['num'])
  inin = input("")

  for course in sem:
    if course['num'] == inin:
      return course['nid']


def course_runner(course):
  activity_monitor(course)
  glance(course)
  print("👤 Your Stats:\n")
  mystats(course, True)
  print("🏆 Leaderboards:\n")
  leaderboards(course)


def get_credentials():

  user = input("Email: ")
  if '@' not in user:
    user += "@uwaterloo.ca"
  password = getpass.getpass("Password: ")

  info = [user,password]
  return info


def overall(a):
  blob = a.get_user_classes()
  n = len(blob) - 1
  p = []
  while (n > 0):
    course = a.network(blob[n]['nid'])
    p.append(mystats(course, False))
    n -= 1
  summed_array = [sum(elements) for elements in zip(*p)]
  #print(summed_array)
  print("👤 Total Stats")
  print("Total Contributions: " + str(summed_array[0]))
  print("Days Online (Note, double-counting): " + str(summed_array[1]))
  print("Questions/Answers: " + str(summed_array[2]) + "/" + str(summed_array[3]))
  print("Posts Viewed: " + str(summed_array[4]))
  print("-"*20)
  print("\n")

def main():
  p = Piazza()
  a = get_credentials()
  p.user_login(a[0], a[1])
  intro(p)
  overall(p)
  while (True):
    b = course_breakdown(p)
    id = semester_breakdown(b)
    course = p.network(id)
    d = course_runner(course)

main()