import requests
from packaging.version import parse

# Replace 'llama_index' with the name of the package you want to find
# package_name = 'llama_index'

# # Find the package's location
# spec = importlib.util.find_spec(package_name)
# if spec is not None:
#     package_path = os.path.dirname(spec.origin)
#     print(f"The package '{package_name}' is located at: {package_path}")
# else:
#     print(f"The package '{package_name}' is not installed.")



package_name = 'llama_index'
url = f'https://pypi.org/pypi/{package_name}/json'

response = requests.get(url)
if response.status_code == 200:
    package_info = response.json()
    latest_version = parse(package_info['info']['version'])
    print(f"The latest version of {package_name} is {latest_version}")
else:
    print(f"Unable to retrieve information for package '{package_name}'.")