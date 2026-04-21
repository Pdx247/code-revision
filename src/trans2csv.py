import json
import pandas as pd
import sys
from config import *

in_path = sys.argv[1]
out_path = sys.argv[2]

try:
    with open(in_path, 'r', encoding = 'utf-8') as f:
        comment = [json.loads(line)['annotated_code'] for line in f]
    with open(CODES_DATA_JSONL_PATH, 'r', encoding = 'utf-8') as f:
        code = [json.loads(line)['source'] for line in f]

    size = len(comment)
    rows = []
    for i in range(size):
        rows.append(
            {
                "source": code[i],
                "comment": comment[i]
            }
        )
    
    df = pd.DataFrame(rows)
    df.to_csv(out_path, encoding = 'utf-8')

except FileNotFoundError:
    print("No such path")