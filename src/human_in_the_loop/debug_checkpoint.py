import sqlite3
import msgpack
import pprint  # For pretty printing

conn = sqlite3.connect("checkpoints.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT checkpoint, metadata FROM checkpoints WHERE thread_id = '888'")  # Adjust the query as needed
rows = cursor.fetchall()

for row in rows:
    checkpoint_data = msgpack.unpackb(row[0])  # Deserialize 'checkpoint'
    metadata_data = msgpack.unpackb(row[1])  # Deserialize 'metadata'

    print("Checkpoint Data:")
    pprint.pprint(checkpoint_data)  # Print in a readable format

    print("\nMetadata Data:")
    pprint.pprint(metadata_data)

conn.close()