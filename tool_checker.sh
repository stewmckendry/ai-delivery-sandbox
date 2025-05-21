grep "module:" /Users/liammckendry/policyGPT/project/reference/tool_catalog.yaml | awk '{print $2}' | sed 's|\.|/|g' | while read -r path; do
  echo "Checking: $path"
  full_path="/Users/liammckendry/policyGPT/${path}.py"
  if [ -f "$full_path" ]; then
    echo "Exists: $full_path"
  else
    echo "Missing: $full_path"
  fi
done