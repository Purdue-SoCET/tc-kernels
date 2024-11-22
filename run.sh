if [ "$#" -ne 1 ]; then
    echo "Must provide assembly file: $0 <input_file>"
    exit 0
fi

SOURCE_FILE=$1

python3 assembler.py $SOURCE_FILE ./temp.bin
python3 softsim/main.py --file ./temp.bin