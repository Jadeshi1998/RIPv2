import Server as s

def test_invalid_command():
    pkt = {
        'header': [1, 2, 12345],  
        'entry': [[54321, 5]]
    }
    try:
        s.check_pkt(pkt)
        print("Invalid command  test , No error raised!!")
    except ValueError:
        print("Invalid command test pass")

def test_invalid_version():
    pkt = {
        'header': [2, 3, 12345],  
        'entry': [[54321, 5]]
    }
    try:
        s.check_pkt(pkt)
        print("Invalid version test , No error raised!!")
    except ValueError:
        print("Invalid version test pass")

def test_invalid_header_length():
    pkt = {
        'header': [2, 2],  
        'entry': [[54321, 5]]
    }
    try:
        s.check_pkt(pkt)
        print("Invalid header length test , No error raised!!")
    except ValueError:
        print("Invalid header length test pass")

def test_empty_entry():
    pkt = {
        'header': [2, 2, 12345],
        'entry': [] 
    }
    try:
        s.check_pkt(pkt)
    except ValueError:
        print("Empty entry test pass")

def test_invalid_destination_id():
    pkt = {
        'header': [2, 2, 12345],
        'entry': [[-1, 5]]  
    }
    try:
        s.check_pkt(pkt)
        print("Invalid destination ID test , No error raised!!")
    except ValueError:
        print("Invalid destination ID test pass")

def test_invalid_metric():
    pkt = {
        'header': [2, 2, 12345],
        'entry': [[54321, 17]] 
    }
    try:
        s.check_pkt(pkt)
        print("Invalid metric test, No error raised!!")
    except ValueError:
        print("Invalid metric test pass")

if __name__ == '__main__':
    test_invalid_command()
    test_invalid_version()
    test_invalid_header_length()
    test_empty_entry()
    test_invalid_destination_id()
    test_invalid_metric()