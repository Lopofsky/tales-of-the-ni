from platform import system

def windows_utf8():
    if system().lower() == 'windows':
        sys.stdout = TextIOWrapper(sys.stdout.detach(), encoding = 'UTF-8')#utf-8
        sys.stderr = TextIOWrapper(sys.stderr.detach(), encoding = 'UTF-8')#utf-8


if __name__ == "__main__":
    windows_utf8()

    print("Greek characters in python have a problem with windows == Οι ελληνικοί χαρακτήρες στην python έχουν πρόβλημα με τα windows.")