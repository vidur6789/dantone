import com.thothink.utils.commonutils as utils


def write_df(file_path, data_frame, sheet_name='Sheet 1'):
    file_path_str = utils.parse_file_path(file_path, "xlsx")
    data_frame.to_excel(file_path_str, sheet_name)
