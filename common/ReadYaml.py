import yaml


class ReadYaml(object):
    def __init__(self, file_path, encoding):
        with open(file_path, "r", encoding=encoding) as file:
            conf_stream = file.read()
        self.configMap = yaml.load(stream=conf_stream, Loader=yaml.FullLoader)

    def get(self, key_path):
        key_arr = key_path.split(".")
        temp_map = self.configMap
        for index in range(len(key_arr)):
            if index != len(key_arr) - 1:
                temp_map = self.configMap[key_arr[index]]
            else:
                return temp_map[key_arr[index]]


if __name__ == "__main__":
    res = ReadYaml("E:\\SubjectNetwork-Download\\resources\\application.yml", "utf-8")
    username = res.get("base-url")
    print(username)

# 获取当前脚本所在文件夹路径
# curPath = os.path.dirname(os.path.realpath(__file__))
# 获取yaml文件路径
# yamlPath = os.path.join(curPath, "cfgyaml.yaml")
