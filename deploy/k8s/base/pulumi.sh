#!/bin/sh

# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Converts the existing Kubernetes YAML file into Pulumi Python Components

# set -x
# set -e
cd "$(dirname $0)"

CURRENT_PATH=$PWD
echo "Current Path: $CURRENT_PATH"

# Define the directory path (you can replace this with your desired path)
K8S_SOURCE_PATH=$CURRENT_PATH

# Check if the directory exists
if [ -d "$K8S_SOURCE_PATH" ]; then
  # Echo the directory path
  echo "Kubernetes Source Path: $K8S_SOURCE_PATH"

  # Create a new directory to store the Pulumi components
  mkdir -p ../pulumi_components

  # Loop through items in the directory
  for item in "$K8S_SOURCE_PATH"/*; do
    # Check if the item is a directory

    if [ -d "$item" ]; then
      # Echo the folder name
      echo "Folder Path: $(dirname \"$item\")"
      echo "Folder: $(basename \"$item\")"
      cd "$item"
      # Run Pulumi Convert
      pulumi convert --from kubernetes --generate-only --language python --out ../../pulumi_components/$(basename $item) -- --component-mode
      cd "$(dirname $0)"

    fi
  done
else
  echo "The directory path '$K8S_SOURCE_PATH' does not exist."
fi
