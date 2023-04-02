import sys
sys.path.append('/Users/lishoulong/Documents/toutiao/lib/openai/myGPTReader')
from utils import get_file_extension

# 示例
filename = "example_document.pdf"
file_extension = get_file_extension(filename)
print("File type:", file_extension)
