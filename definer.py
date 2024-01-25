import re
from io import TextIOWrapper
from pathlib import Path

NOTES_DIRECTORY = Path.cwd() / "Notes"
DEFINITIONS_DIRECTORY = Path.cwd() / "Definitions"

# TODO: probably redo everything (string mess with remove suffix and prefix and whatnot), work on a copy of notes, not the real stuff.


def extract_definition(line: str) -> tuple[str, str]:
    split = line.split(": ")
    # Remove \t, -, and \n
    return (re.sub("[\\t-]", "", split[0])[1:], split[1].removesuffix("\n"))


def find_words(file: Path) -> list[tuple[str, str]]:
    words = []
    with open(file) as f:
        for line in f.readlines():
            if ":" in line and "-" in line:
                words.append(extract_definition(line))  # TODO: fix [[ ]]

    return words


def create_definition_file(word: str, definition: str):
    if Path.exists(
        DEFINITIONS_DIRECTORY / f"{word.removeprefix('[[').removesuffix(']]')}.md"
    ):
        return

    with open(DEFINITIONS_DIRECTORY / f"{word}.md", "w") as f:
        f.write(definition)

    print(f"Created '{word}'")


def create_definitions():
    for file in NOTES_DIRECTORY.glob("**/*.md"):
        words = find_words(file)
        for word, definition in words:
            create_definition_file(word, definition)


def get_known_definitions() -> list[str]:
    definitions = []
    for file in DEFINITIONS_DIRECTORY.glob("**/*.md"):
        definitions.append(file.name.removesuffix(".md").lower())

    return definitions


def find_index_of_first_nonalphanum(string: str) -> int:
    for index, char in enumerate(string):
        if not char.isalnum():
            return index
    return -1


def connect_definitions():
    knownDefinitions = get_known_definitions()
    for file in NOTES_DIRECTORY.glob("**/*.md"):
        with open(file, "r") as f:
            data = f.read()

        data = data.split(" ")
        for i in range(len(data)):
            word = re.sub("[^A-Za-z0-9 \[ \]]+", "", data[i]).lower()
            if word in knownDefinitions and ("[[" not in word or "]]" not in word):
                if data[i][-1].isalnum():
                    data[i] = f"[[{data[i]}]]"
                else:
                    index = find_index_of_first_nonalphanum(data[i])
                    data[i] = f"[[{data[i][:index]}]]{data[i][index:]}"
        data = " ".join(data)

        with open(file, "w") as f:
            f.write(data)


def main():
    create_definitions()
    connect_definitions()


if __name__ == "__main__":
    main()
