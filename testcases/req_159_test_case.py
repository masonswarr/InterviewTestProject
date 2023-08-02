# API import. Full import path denoted as <...>
import <...>.backend_api as b_api

import time


# Valid and invalid email address lists
VALID_ADDRESSES = [
                   'valid_user_1@server.com',
                   'valid_user_2@server.com',
                   'valid_user_3@server.com'
                  ]

INVALID_ADDRESSES = [
                     'invalid_user_1',
                     'invalid_user_2@nope',
                     'invalid_user_3@.nope'
                    ]


class Req159Test():
    """
        Class responsible for setting up, running, and tearing down the tests needed for requirement 159.
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
            raise Exception('Req. 159 test FAILED:\n{}'.format(e))


    def __del__(self):
        """
            Class destructor. Logs out of the user session.
        """
        self.user_session.logout()


    def run(self):
        """
            Method to run the subtests.

        Args:
            None

        Returns:
            None

        Raises:
            Exception   : If any test step for requirement 159 fails
        """
        # ASSUMPTION: The received and sent email lists are empty prior to this test

        ### STEP 1: Send an email with valid addresses in the To, Cc, and Bcc lines ###
        # ASSUMPTION: A simple "send_email" method with valid default values is available in the API.
        # Actual method to send emails with the API could differ.
        self.user_session.send_email(to_list=[VALID_ADDRESSES[0]],
                                     cc_list=[VALID_ADDRESSES[1]],
                                     bcc_list=[VALID_ADDRESSES[2]])
        
        # Wait for sending to complete. The actual sleep time would need to come from the design team.
        time.sleep(...)

        ### STEP 2: Make sure each valid address is in the sent mail list ###
        # ASSUMPTION: The value returned by the "get_sent_mail_list" return a list of dictionaries, representing each email present in the sent list.
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
        sent_mail = self.user_session.get_sent_mail_list()

        # Pull recipient addresses from the sent emails using double list comprehension
        recipient_list = [address for email in sent_mail for address in email['to'] + email['cc'] + email['bcc']]

        # Get list of valid addresses that are NOT in the list of recipients
        valid_addresses_not_present = [address for address in VALID_ADDRESSES if address not in recipient_list]

        # Clear sent list in the database prior to check
        # ASSUMPTION: A "clear_sent_list" method is available in the API. If not, filtering the emails by timestamp could be an option.
        self.user_session.clear_sent_list()

        # Check if any valid addresses were missing from the recipient list. If so, fail this test.
        if valid_addresses_not_present:
            raise Exception('Req. 159 test FAILED:\nReason:\nEmail failed to send to valid address(es) during valid address subtest; {}'.format(', '.join(valid_addresses_not_present))

        ### STEP 3: Send email with both valid and invalid addresses in the To, Cc, and Bcc lines ###
        self.user_session.send_email(to_list=[VALID_ADDRESSES[0], INVALID_ADDRESSES[0]],
                                     cc_list=[VALID_ADDRESSES[1], INVALID_ADDRESSES[1]],
                                     bcc_list=[VALID_ADDRESSES[2], INVALID_ADDRESSES[2]])

        # Wait for sending to complete. The actual sleep time would need to come from the design team.
        time.sleep(...)

        ### STEP 4: Make sure each valid address is in the sent mail list ###
        sent_mail = self.user_session.get_sent_mail_list()

        # Pull recipient addresses from the sent emails using double list comprehension
        recipient_list = [address for email in sent_mail for address in email['to'] + email['cc'] + email['bcc']]

        # Get list of valid addresses that are NOT in the list of recipients
        valid_addresses_not_present = [address for address in VALID_ADDRESSES if address not in recipient_list]

        # Clear sent list in the database prior to checks
        self.user_session.clear_sent_list()

        # Check if any valid addresses were missing from the recipient list. If so, fail this test.
        if valid_addresses_not_present:
            raise Exception('Req. 159 test FAILED:\nReason:\nEmail failed to send to valid address(es) during step 4; {}'.format(', '.join(valid_addresses_not_present))

        ### STEP 5: Make sure each invalid address is not in the sent mail list ###
        # Get list of invalid addresses that are in the list of recipients
        invalid_addresses_present = [address for address in INVALID_ADDRESSES if address in recipient_list]

        # Check if any valid addresses were missing from the recipient list. If so, fail this test.
        if invalid_addresses_present:
            raise Exception('Req. 159 test FAILED:\nReason:\nEmail sent to invalid address(es) during invalid address subtest; {}'.format(', '.join(invalid_addresses_present))
