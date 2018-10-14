import sys

class FBPoolError:

    @staticmethod
    def exit_with_error(operation,fbapi_exception=None,additional_message=None):
        FBPoolError.__print_error(operation,fbapi_exception,additional_message)
        sys.exit(1)

    @staticmethod
    def error_no_exit(operation,fbapi_exception=None,additional_message=None):
        FBPoolError.__print_error(operation,fbapi_exception,additional_message)

    @staticmethod
    def load_error(name,fbapi_exception):
        operation = "loading %s" % (name)
        additional_message = "Database data may be in invalid state."
        FBPoolError.exit_with_error(operation,fbapi_exception,additional_message)

    @staticmethod
    def delete_error(name,fbapi_exception=None,additional_message=None):
        operation = "deleting %s" % (name)
        FBPoolError.exit_with_error(operation,fbapi_exception,additional_message)

    @staticmethod
    def __print_line(length):
        s = ""
        for i in range(length):
            s += "-"
        print(s)

    @staticmethod
    def __print_error(operation,fbapi_exception=None,additional_message=None):
        title = "**ERROR** Encountered error when %s" % (operation)

        print("")
        print(title)
        FBPoolError.__print_line(len(title))

        if fbapi_exception:
            print("FBAPIException: code=%d, msg=%s" % (fbapi_exception.http_code,fbapi_exception.errmsg))

        if additional_message:
            print(additional_message)

        print("")
