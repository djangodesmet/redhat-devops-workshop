#!/bin/bash

# Replaces env variables declared in .gitlab_ci.yaml

# Find all Chart.yaml and values.yaml files in the current directory and subdirectories
find ./helm-deployments -type f \( -name "Chart.yaml" -o -name "values.yaml" \) | while read -r file; do

  # Create a temporary file to store the substituted content
  tmp_file=$(mktemp)

  # Substitute the environment variables and write to the temporary file
  envsubst '${API_APP_NAME} ${STREAMLIT_APP_NAME} ${NAMESPACE} ${IMAGE_TAG}' < "$file" > "$tmp_file"

  # Move the temporary file to the original file
  mv "$tmp_file" "$file"
done
