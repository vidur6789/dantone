from collections import namedtuple

Column = namedtuple('Column', 'index, name')
Response = namedtuple("Response", "data, errors")
Error = namedtuple("Error", "ticker, exception")
OutputVariable = namedtuple("OutputVariable", "name, period")
