from pathlib import Path

from com.thothink.constants.constant import PATH_TMP


def write_errors(errors):
    error_lines = []
    with open(str(PATH_TMP / "logs.txt"), "w") as write_file:
        for error in errors:
            error_lines.append("Error occured for :" + error.ticker)
            error_lines.append("Error message : " + error.message)
            error_lines.append("Arguments: " + str(error.args))
        write_file.writelines(error_lines)
