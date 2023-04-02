import os

import importlib.util
import os


# Replace 'llama_index' with the name of the package you want to find
package_name = 'pydub'

# Find the package's location
spec = importlib.util.find_spec(package_name)
if spec is not None:
    package_path = os.path.dirname(spec.origin)
    print(f"The package '{package_name}' is located at: {package_path}")
else:
    print(f"The package '{package_name}' is not installed.")


