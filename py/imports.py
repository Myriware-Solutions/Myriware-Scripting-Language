import urllib.request
from outter import Outter
# urllib.request.urlretrieve("http://www.example.com/songs/mp3.mp3", "mp3.mp3")

class Imports:
    def get(importPath: str):
        import_path = importPath
        Outter.out('sec', "Attemping to download: " + import_path)
        github_url = "https://raw.githubusercontent.com/Myriware-Solutions/mslimports/main"
        package_module = import_path.split("/")
        type = ""
        match package_module[0]:
            case "lang":
                type = "lang"
                destination = "./msl/lang/"
            case "module":
                type = "py"
                destination = "./msl/imports/"
        file_name = f"{package_module[1]}.{type}"
        url = f"{github_url}/{package_module[0]}/{file_name}"
        Outter.out('sec', "Requesting URL: " + url)
        urllib.request.urlretrieve(url, destination + file_name)

    def run(module: str, function: str):
        print("jj")