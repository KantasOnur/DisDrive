ATTACHMENT_SIZE = 25000000


def readFile():
    with open(sys.argv[1], "rb") as f:
        contents = f.read()
    f.close()
    return contents


def chunkifyFile(contents, fileName, size, numFiles):
    firstByte = 0
    lastByte = size  # either 25k or end of file
    if size > ATTACHMENT_SIZE:
        lastByte = ATTACHMENT_SIZE

    for writeFiles in range(numFiles):

        subContents = contents[firstByte:lastByte]
        contents = contents[lastByte:size]

        with open(f"output/{fileName.split('.')[0]}_{writeFiles}.txt", "wb") as outF:
            outF.write(subContents)

        lastByte = size - lastByte  # either add 25k or end of file

        if lastByte > ATTACHMENT_SIZE:
            lastByte = ATTACHMENT_SIZE


def main():
    contents = readFile()

    fileName = sys.argv[1].split('/')[-1]
    size = len(contents)
    numFiles = ceil(size / ATTACHMENT_SIZE)

    chunkifyFile(contents, fileName, size, numFiles)


if __name__ == "__main__":
    from math import ceil
    import sys

    main()
