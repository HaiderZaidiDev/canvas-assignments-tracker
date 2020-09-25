# canvas-assignments-to-excel
Goes through all of the courses a student is enrolled in on Canvas, and records the assignments and their due dates in a spreadsheet.

## Ideology
I noticed quite a bit of people at my university spent multiple hours going through their Canvas by hand, adding all of their assignments in a spread sheet to help them keep track of what needed to be done. I felt that this process could be automated, so I went ahead and did it.

## Use
Before use, you need to create an access token on Canvas. To do this go to your profile on Canvas, click settings, then scroll down to approved integrations and create an access token. 

If you're at Schulich, you can use this link: https://schulich.instructure.com/profile/settings (If you're at another school just replace the starting part of the link with your school's link).

Once you have your access token, set it as an environment variable on your device under the name "CANVAS_API_KEY", or you can just replace the environment variable in the script with a string of your access token.

## Demo
Here's an example of what the spreadsheet looks like with my schedule.

![Spreadsheet Screenshot](https://i.imgur.com/St3tWkZ.png)

## To-do
- [ ] Create a front-end website so student's who aren't familiar with Python can still download spreadsheets.
- [ ] OAuth2 Integration, will likely come with the front-end. Currently awaiting approval from the Schulich I.T department

