# Import requirements test cases with import paths denoted as <...>
from <...>.testcases.req_42_test_case import Req159Test
from <...>.testcases.req_159_test_case import Req42Test

import argparse


def main():
    # Setup parser for user input and gather arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_email", help="Email address for test account", default='user_name@server.com')
    parser.add_argument("--user_pwd", help="Password for test account", default='password123')
    parser.add_argument("--failfast", help="Flag determining if testing should halt on first failure", action="store_true")
    args = parser.parse_args()

    failfast = args.failfast
    user_name = args.user_email
    user_pwd = args.user_pwd

    # List of test objects.
    test_objects = [Req159Test, Req42Test]
    
    # Loop on the test objects. Creates the object and calls the object's run() method
    for test_object in test_objects:
        try:
            test_object(user_name, user_pwd).run()
        except Exception as e:
            if failfast:
                raise
            else:
                # Log the failure using caught exception 'e' and continue


if __name__ == "__main__":
    main()
