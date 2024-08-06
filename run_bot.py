

def main():
    print("READY")
    state = input()
    with open("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com.log", "w") as log_file:
        log_file.write(state)
    print("START Watcher 0")
    print(state)


if __name__ == '__main__':
    main()
