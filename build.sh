#!/bin/bash

set -e  # exit on error

SRC_PATH="./src/"
SRC_BASHSCRIPT_NAMR="netcheck.sh"
DELIVERY_PATH="./dist/"
DELIVERY_BASHSCRIPT_NAME="netcheck.sh"
DELIVERY_PYTHONSCRIPT_NAME="netcheck.py"

SRC_CONFIG="config.json"
SRC_BASHSCRIPT="${SRC_PATH}${SRC_BASHSCRIPT_NAMR}"
DEST_CONFIG="${DELIVERY_PATH}config.json"
DEST_BASHSCRIPT="${DELIVERY_PATH}${DELIVERY_BASHSCRIPT_NAME}"
DEST_PYTHONSCRIPT="${DELIVERY_PATH}${DELIVERY_PYTHONSCRIPT_NAME}"

# 0. clean the folder
echo "Cleaning up the folder..."
rm -rf "$DELIVERY_PATH"* 2>/dev/null

#1.1. deliver config file
echo "Copying the config file"
cp "$SRC_CONFIG" "$DEST_CONFIG"

#1.2. deliver bash script
echo "Copying the bash script"
cp "$SRC_BASHSCRIPT" "$DEST_BASHSCRIPT"

#1.3. deliver .py script
echo "Building the .py script"
echo "Calling pinliner..."
python src-make/lib/pinliner/pinliner/pinliner.py src -o "${DEST_PYTHONSCRIPT}"
echo "Patching mdmtoolsap_bundle.py..."
echo "# ..." >> "${DEST_PYTHONSCRIPT}"
echo "# print('within mdmtoolsap_bundle')" >> "${DEST_PYTHONSCRIPT}"
# REM REM :: no need for this, the root package is loaded automatically
# echo "# import mdmtoolsap_bundle" >> "${DEST_PYTHONSCRIPT}"
echo "from src import launcher" >> "${DEST_PYTHONSCRIPT}"
echo "launcher.main()" >> "${DEST_PYTHONSCRIPT}"
echo "# print('out of mdmtoolsap_bundle')" >> "${DEST_PYTHONSCRIPT}"
echo "Done with pinliner"

#2. make updates to paths
echo "Rename and update paths..."
tmp_file="$(mktemp)"

sed 's|\./tests/|../tests/|g' "$DEST_BASHSCRIPT" > "$tmp_file"
mv "$tmp_file" "$DEST_BASHSCRIPT"

echo "Done. Build script has finished."
