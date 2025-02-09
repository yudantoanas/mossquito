from utils import scrape, files_copier, notebook_extractor

if __name__ == "__main__":
    url = input("GitHub Classroom Assignment Url: ")
    prefix = input("Assignment Repository Prefix Url: ")

    data = scrape(url, prefix)
    print(data)

    while True:
        print("Select file format:")
        print("1. .py")
        print("2. .ipynb")
        print()

        args = input("select: ")
        if args.lower() == "1":
            files_copier(data)
            break
        elif args.lower() == "2":
            notebook_extractor(data)
            break
        else:
            print("Wrong selection! Try again.")