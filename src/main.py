from src.tasks import textract_from_file, textract_from_raw_bytes
import pickle
import sys

if __name__ == '__main__':
    test_file_path = sys.argv[1]
    result = textract_from_file.delay(test_file_path, "test.csv")

    while not result.ready():
        pass
    print(result.ready())
    r = result.get()
    r = r[0]
    pickled_data = pickle.dumps(r)

    result = textract_from_raw_bytes.delay(pickled_data)
    while not result.ready():
        pass
    print(result.ready())