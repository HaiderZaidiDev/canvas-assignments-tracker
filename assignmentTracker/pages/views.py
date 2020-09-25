from django.shortcuts import render
from .forms import AccessTokenForm

from canvasapi import Canvas
from datetime import datetime
from openpyxl import load_workbook
import os
import mimetypes
from django.http import HttpResponse


def retrieveAssignments(course, token):
    """ Retrieves all the assignments for a course, and related info. """
    API_URL = "https://schulich.instructure.com/"
    # Change this link based on the School you attend.
    API_KEY = token
    canvas = Canvas(API_URL, token)
    # Initialize a new Canvas object

    course = canvas.get_course(course)
    assignments = course.get_assignments()
    courseAssignments = {}
    currentAssignment = {}
    for assignment in assignments:
        name = assignment.name
        dueDateRaw = assignment.due_at
        # Unpacking and formatting date.
        if dueDateRaw is None: # Usually if due date hasn't been set.
            dueDate = dueTime = "N/A"
        else:
            dueDateObj = datetime.strptime(dueDateRaw, '%Y-%m-%dT%H:%M:%SZ')
            dueDate = dueDateObj.strftime("%Y-%m-%d")
            dueTime = dueDateObj.strftime("%H:%M")

        weight = assignment.points_possible
        assignmentInfo = {
            "course":course.name[0:11],
            "dueDate": dueDate,
            "dueTime": dueTime,
            "weight": weight
        }
        currentAssignment[name] = assignmentInfo
        courseAssignments.update(currentAssignment)
    return courseAssignments

def writeToSheet(token):
    """ Writes all assignment information to a spreadsheet."""
    API_URL = "https://schulich.instructure.com/"
    # Change this link based on the School you attend.
    API_KEY = token
    canvas = Canvas(API_URL, token)

    workbook = load_workbook(filename='pages/sheets/master-sheets/Canvas Assignments (Master).xlsx')
    sheet = workbook.active
    allCourses = canvas.get_courses()
    courseIDS = []
    count = 1

    # Getting IDS of all courses the user is enrolled in
    for items in allCourses:
        if items.id != 3967: # Schulich Academic Dishonesty Course
            courseIDS.append(items.id)
    for i in range(len(courseIDS)):
        assignments = retrieveAssignments(courseIDS[i], token)
        for assignment, info in assignments.items():
            count += 1
            sheet.cell(row=count, column=7, value=assignment)
            sheet.cell(row=count, column=4, value=info['course'])
            sheet.cell(row=count, column=1, value=info['dueDate'])
            sheet.cell(row=count, column=3, value=info['dueTime'])
            sheet.cell(row=count, column=11, value=info['weight'])
    workbook.save(filename="pages/sheets/user-sheets/Canvas-Assignments ({}).xlsx".format(token[5:10]))
    #Slices characters for differentiation of filename.


def homeView(request):
    """ Renders home page, serves spreadsheet to user """
    form = AccessTokenForm(request.POST or None)
    if form.is_valid():
        form.save()
        tokenClean = form.cleaned_data['token']
        sheetName = "Canvas-Assignments ({}).xlsx".format(tokenClean[5:10])
        writeToSheet(tokenClean)
        # Serving spreadsheet.
        with open("pages/sheets/user-sheets/{}".format(sheetName),'rb') as spreadsheet:
            sheet = spreadsheet.read()
            response = HttpResponse(sheet)
            response['Content-Type'] = 'mimetype/submimetype'
            response['Content-Disposition'] = 'attachment; filename={}'.format(sheetName)
            return response
        print('update')
    return render(request, 'index.html', {'form':form})
# Create your views here.
