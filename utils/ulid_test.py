from ulid import ULID

for i in range(0, 100):
    # Generate a ULID
    ulid = ULID()

    print("ULID:", ulid.generate())
