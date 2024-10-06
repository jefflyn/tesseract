import pandas as pd

data = {'johnny\
newline': 2, 'alice': 3, 'bob': 3,
        'frank': 4, 'lisa': 1, 'tom': 8}
n = range(1, max(data.values()) + 1)

# Create DataFrame with columns = pos
output = pd.DataFrame(columns=n, index=[])

# Populate DataFrame with rows
for index, (bidder, pos) in enumerate(data.items()):
    output.loc[index, pos] = bidder

# Print the DataFrame and remove NaN to make it easier to read.
print(output.fillna(''))

# Fetch and print every element in column 2
for index in range(1, 5):
    print(output.loc[index, 2])