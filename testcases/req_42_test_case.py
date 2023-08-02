# API import. Full import path denoted as <...>
import <...>.backend_api as b_api

import time


class Req42Test():
    """
        Class responsible for setting up, running, and tearing down the tests needed for requirement 42.
    """
    def __init__(self, user_name, user_pwd):
        """
            Class initiator: Attempts to create a user session using the provided credentials.

        Args:
            user_name   : String    : User name
            user_pwd    : String    : User password

        Returns:
            None

        Raises:
            Exception   : If unable to login using the provided credentials
        """
        try:
            # ASSUMPTION: A "login" method or some way to create a session with a given user is available in the API.
            self.user_session = b_api.login(user=user_name, pwd=user_pwd)
        except Exception as e:
            raise Exception('Req. 42 test FAILED:\n{}'.format(e))


    def __del__(self):
        """
            Class destructor. Clears mail list, the spam address list, and logs out of the user session.
        """
        # Clear inbox, spam mail, and spam address lists
        # ASSUMPTION: "clear_received_list", "clear_spam_email_list", and "clear_spam_address_list" method are available in the API.
        self.user_session.clear_received_list()
        self.user_session.clear_spam_email_list()
        self.user_session.clear_spam_address_list()

        # Logout of user session
        self.user_session.logout()


    def run(self):
        """
            Method to run the subtests.

        Args:
            None

        Returns:
            None

        Raises:
            Exception   : If any test step for requirement 42 fails
        """
        # ASSUMPTION: The received and sent email lists are empty along prior to this test
        # ASSUMPTION: The spam emails are contained in a list separate from the rest of the received emails.

        # Sender email address
        sender_address = 'sender@tester.com'

        ### STEP 1: Receive an email from a test address that is not in the spam list ###
        # ASSUMPTION: The ability to simulate receiving an email from the in-bound mail server exists and is available in the API.
        b_api.receive_email_from_in_bound_mail_server(sender=sender_address, to_list=[self.user_session.get_email()])

        ### STEP 2: Make sure email from sender_address is not sent to the spam list ###
        # ASSUMPTION: The value returned by the "get_spam_mail_list" return a list of dictionaries, representing each email present in the inbox.
        # Format is assumed to be the following;
        #   [
        #       { 
        #           'to': [],
        #           'cc': [],
        #           'bcc': [],
        #           'sender': '',
        #           'subject': '',
        #           'message': '',
        #           ...
        #       },
        #       ...
        #   ]
        spam_email_list = self.user_session.get_spam_mail_list()

        # Get spam emails with sender_address as the sender
        spam_sender_list = [email for email in spam_email_list if email['sender']==sender_address]

        # Check if sender_address is in the spam_sender_list. If present, fail.
        if sender_address in spam_sender_list:
            raise Exception('Req. 42 test FAILED:\nReason:\nReceived email sent to spam list during step 2')

        ### STEP 3: Add test address to the spam list ###
        # Add sender_address to user_session's spam list
        # ASSUMPTION: An add_address_to_spam_list method is available in the API
        self.user_session.add_address_to_spam_list(sender_address)

        ### STEP 4: Check if email is present in the spam folder ###
        # ASSUMPTION: The backend application automatically scrubs the inbox for emails with addresses in the spam list and
        #             does not only check incoming emails. If the inbox is not automatically scrubbed, triggering a scrub or
        #             sending another email are other options.

        # Wait for automatic scrub to complete. The actual sleep time would need to come from the design team.
        time.sleep(...)

        # Refresh spam email list
        spam_email_list = self.user_session.get_spam_mail_list()

        # Get spam emails with sender_address as the sender
        spam_sender_list = [email for email in spam_email_list if email['sender']==sender_address]

        # Check if sender_address is not in the sender_list. If not present, fail.
        if sender_address not in spam_sender_list:
            raise Exception('Req. 42 test FAILED:\nReason:\nReceived email not sent to spam list during step 4')
