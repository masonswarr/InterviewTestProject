# Project Overview

This is a project written for the second stage of the interview process at Outside Analytics. The purpose is to showcase my coding expertise and demonstrate how I would design the tests for the given requirements of an email application system.

# Testing Approach
A Black-Box testing approach was taken for this project.

# Testing Structure
The structure for the overall test is as follows;
 - A main script written in Python V3. This is the main entry point for the test itself. It gathers user inputs and calls each test case with the proper inputs.
 - Multiple test cases, kept separately from the main script in the "testscases" folder. For each requirement to be tested, a test case will be created.

# Assumptions
### Overall Infrastructure
 - An isolated test environment is being used
 - A brand new user account has been created in this test system
 - The received email, sent email, and spam address lists for the test user are empty prior to testing
 - The spam emails in the database are contained in a list separate from the rest of the received emails

### Backend Application
 - A Python V3 API is available for the backend application
 - The backend application does not prevent sending emails with any invalid address in the To, Cc, and Bcc lines
 - The backend application automatically scrubs the inbox for emails with addresses in the spam list and does not only check incoming emails

### Backend API (Also documented in the relevant test case files)
 - A "login" method or some way to create a session with a given user is available
 - A "send_email" method with valid default values is available
 - The value returned by the "get_sent_mail_list" return a list of dictionaries, representing each email present in the sent list.
   The format of this list is assumed to be the following;
   ```
     [
       { 
         'to': [],
         'cc': [],
         'bcc': [],
         'sender': '',
         'subject': '',
         'message': '',
         ...
       },
       ...
     ]
   ```
 - A "clear_sent_list" method is available
 - A "clear_received_list" method is available
 - A "clear_spam_email_list" method is available
 - A "clear_spam_address_list" method is available
 - The value returned by the "get_spam_mail_list" return a list of dictionaries, representing each email present in the inbox with the same format specified above
 - An "add_address_to_spam_list" method is available

# Test Steps
Listed below are the descriptions of requirement and test steps needed to verify.
## Requirement #159
#### Description: Email shall be sent to any valid email address from To, Cc, and/or Bcc address lines
#### Test Steps
1. Use API to send an email with valid addresses in the To, Cc, and Bcc lines
2. Make sure emails with the valid addresses are present in the sent email list in the database. If not all valid addresses are present, fail.
3. Use API to "send" emails with an invalid address in To, Cc, and Bcc address lines along with a valid address in each line.
4. Make sure emails with valid addresses are present in the sent email list in the database. If not all valid addresses are present, fail.
5. Make sure emails with invalid addresses are not present in the sent email list in the database. If any invalid address is present, fail.

### Requirement #42
#### Description: All email addresses identified as spam by the user shall be automatically sent to the spam folder
#### Test Steps
1. Use API to "receive" an email from a test address that is not in the spam list
2. Check if email is present in the spam folder in the database. If present, fail.
3. Add test address to the spam list
4. Check if email is present in the spam folder. If not present, fail.

# Missing Features
For this small testing suite to be complete, the following features would need to be added;
## 1. Logging
  Proper logging of user inputs, testing status, and any errors or warnings is a must. Decorators and error handlers would need to be implemented. The logs would also need to be formatted in an easy-to-read way and made available during and post testing.
## 2. Test interface
  To help prevent user error on the command line, a simple GUI is needed.
## 3. A proper test framework
  Instead of simulating a test framework, utilizing a known and well-documented test platform like Avocado or Cucumber would provide many short-term and long-term benefits.
