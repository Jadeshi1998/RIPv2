import sys
import Server as s

#python3 main.py router1.txt


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <config_filename>")
        sys.exit(1)

    config_filename = sys.argv[1]
    s.main(config_filename)

if __name__ == '__main__':
    main()