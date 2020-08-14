import com.thothink.read.XlsReader as reader
import com.thothink.write.JsonFileWriter as writer
import com.thothink.constants.constant as constant
import ast


data = reader.parse_as_records(constant.PATH_OUT / "Top100.xlsx", sheet_name="raw-data")
print(len(data))
for item in data:
    print(item['keywords'])
    keywords = ast.literal_eval(item['keywords']) if item['keywords'] != '-' else []
    item['keywords'] = keywords

print(len(data))
writer.write(constant.PATH_OUT / "tripadvisor5", data[0:5])


