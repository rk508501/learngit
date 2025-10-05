name: 17 - Debugging and Monitoring

on:
  push:
  workflow_dispatch:
    inputs:
      debug_enabled:
        description: 'Enable debug logging'
        required: false
        type: boolean
        default: false

jobs:
  debug-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Enable debug logging
        if: inputs.debug_enabled || runner.debug == '1'
        run: |
          echo "::debug::Debug mode is enabled"
          echo "Debug information will be shown"
      
      - name: Display context information
        run: |
          echo "::group::GitHub Context"
          echo "Event: ${{ github.event_name }}"
          echo "Repository: ${{ github.repository }}"
          echo "Actor: ${{ github.actor }}"
          echo "SHA: ${{ github.sha }}"
          echo "Ref: ${{ github.ref }}"
          echo "Workflow: ${{ github.workflow }}"
          echo "::endgroup::"
      
      - name: Display runner context
        run: |
          echo "::group::Runner Context"
          echo "OS: ${{ runner.os }}"
          echo "Arch: ${{ runner.arch }}"
          echo "Temp: ${{ runner.temp }}"
          echo "Tool cache: ${{ runner.tool_cache }}"
          echo "::endgroup::"
      
      - name: Set outputs
        id: demo-step
        run: |
          echo "result=success" >> $GITHUB_OUTPUT
          echo "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_OUTPUT
      
      - name: Use step outputs
        run: |
          echo "Result: ${{ steps.demo-step.outputs.result }}"
          echo "Timestamp: ${{ steps.demo-step.outputs.timestamp }}"
      
      - name: Create annotations
        run: |
          echo "::notice::This is a notice annotation"
          echo "::warning::This is a warning annotation"
          # echo "::error::This is an error annotation"
      
      - name: Group output
        run:
