import sys
import Server as s

#python3 main.py ../router/router1.txt
#python3 main.py ../router/router2.txt
#python3 main.py ../router/router3.txt
#python3 main.py ../router/router4.txt
#python3 main.py ../router/router5.txt
#python3 main.py ../router/router6.txt
#python3 main.py ../router/router7.txt


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <config_filename>")
        sys.exit(1)

    config_filename = sys.argv[1]
    s.main(config_filename)

if __name__ == '__main__':
    main()