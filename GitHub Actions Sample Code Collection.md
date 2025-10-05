GitHub Actions Sample Code Collection
Complete code samples for each lesson in the GitHub Actions Learning Plan.

Week 1: Foundations
Day 1-2: First Workflow - Hello World
File: .github/workflows/01-hello-world.yml

name: 01 - Hello World

# Trigger on push to any branch
on: [push]

jobs:
  greeting:
    runs-on: ubuntu-latest
    steps:
      - name: Say hello
        run: echo "Hello, GitHub Actions!"
      
      - name: Display date
        run: date
      
      - name: Show working directory
        run: pwd
Day 3-4: Multiple Triggers
File: .github/workflows/02-multiple-triggers.yml

name: 02 - Multiple Triggers

# Multiple event triggers
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
  schedule:
    # Run every day at 2:30 AM UTC
    - cron: '30 2 * * *'
  workflow_dispatch:  # Manual trigger

jobs:
  log-event:
    runs-on: ubuntu-latest
    steps:
      - name: Display event type
        run: echo "Triggered by ${{ github.event_name }}"
      
      - name: Display branch
        run: echo "Branch is ${{ github.ref }}"
      
      - name: Display actor
        run: echo "Triggered by ${{ github.actor }}"
Day 5-7: Jobs and Steps
File: .github/workflows/03-jobs-and-steps.yml

name: 03 - Jobs and Steps

on: [push]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: List files
        run: ls -la
      
      - name: Display commit message
        run: echo "Latest commit - ${{ github.event.head_commit.message }}"
  
  build:
    runs-on: ubuntu-latest
    needs: setup  # Wait for setup job to complete
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Simulate build
        run: |
          echo "Building application..."
          sleep 2
          echo "Build completed!"
  
  test:
    runs-on: ubuntu-latest
    needs: build  # Wait for build job to complete
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run tests
        run: |
          echo "Running tests..."
          sleep 2
          echo "All tests passed!"
  
  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]  # Wait for both jobs
    if: github.ref == 'refs/heads/main'  # Only on main branch
    steps:
      - name: Deploy application
        run: echo "Deploying to production..."
Week 2: Practical Applications
Day 8-10: Node.js CI Pipeline
File: .github/workflows/04-nodejs-ci.yml

name: 04 - Node.js CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build project
        run: npm run build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-files
          path: dist/
          retention-days: 7
Day 8-10: Python CI Pipeline
File: .github/workflows/05-python-ci.yml

name: 05 - Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      
      - name: Run linter
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Run tests with coverage
        run: pytest --cov=./ --cov-report=xml
      
      - name: Upload coverage reports
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml
Day 11-13: Environment Variables and Secrets
File: .github/workflows/06-secrets-and-env.yml

name: 06 - Secrets and Environment Variables

on: [push]

env:
  GLOBAL_VAR: "I am global"
  APP_NAME: "MyAwesomeApp"

jobs:
  use-secrets:
    runs-on: ubuntu-latest
    env:
      JOB_VAR: "I am job-level"
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Display environment variables
        env:
          STEP_VAR: "I am step-level"
        run: |
          echo "Global var: $GLOBAL_VAR"
          echo "Job var: $JOB_VAR"
          echo "Step var: $STEP_VAR"
          echo "App name: $APP_NAME"
      
      - name: Use secrets (masked in logs)
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          echo "API Key is set: ${API_KEY:+YES}"
          echo "Database URL is set: ${DATABASE_URL:+YES}"
          # Never echo actual secret values!
      
      - name: Use GitHub context
        run: |
          echo "Repository: ${{ github.repository }}"
          echo "Actor: ${{ github.actor }}"
          echo "SHA: ${{ github.sha }}"
          echo "Ref: ${{ github.ref }}"
          echo "Event: ${{ github.event_name }}"
      
      - name: Conditional based on environment
        if: github.ref == 'refs/heads/main'
        run: echo "Running on main branch"
Day 14: Matrix Builds
File: .github/workflows/07-matrix-builds.yml

name: 07 - Matrix Builds

on: [push, pull_request]

jobs:
  test-matrix:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
        # This creates 9 jobs: 3 OS × 3 Node versions
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Display environment
        run: |
          echo "OS: ${{ matrix.os }}"
          echo "Node version: ${{ matrix.node-version }}"
          node --version
          npm --version
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test

  test-matrix-advanced:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false  # Continue other jobs if one fails
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']
        include:
          # Add extra configuration for specific combinations
          - os: ubuntu-latest
            python-version: '3.11'
            experimental: true
        exclude:
          # Skip this specific combination
          - os: macos-latest
            python-version: '3.9'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Display info
        run: |
          echo "OS: ${{ matrix.os }}"
          echo "Python: ${{ matrix.python-version }}"
          echo "Experimental: ${{ matrix.experimental }}"
          python --version
Week 3: Advanced Techniques
Day 15-17: Composite Action
File: .github/actions/setup-app/action.yml

name: 'Setup Application'
description: 'Composite action to setup Node.js app with caching'

inputs:
  node-version:
    description: 'Node.js version to use'
    required: false
    default: '20'
  install-dependencies:
    description: 'Whether to install dependencies'
    required: false
    default: 'true'

outputs:
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.cache-deps.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    
    - name: Cache dependencies
      id: cache-deps
      uses: actions/cache@v4
      with:
        path: ~/.npm
        key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      shell: bash
    
    - name: Install dependencies
      if: inputs.install-dependencies == 'true'
      run: npm ci
      shell: bash
    
    - name: Display versions
      run: |
        echo "Node version: $(node --version)"
        echo "NPM version: $(npm --version)"
      shell: bash
File: .github/workflows/08-use-composite-action.yml

name: 08 - Use Composite Action

on: [push]

jobs:
  use-composite:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup application
        id: setup
        uses: ./.github/actions/setup-app
        with:
          node-version: '20'
          install-dependencies: 'true'
      
      - name: Check cache status
        run: echo "Cache hit - ${{ steps.setup.outputs.cache-hit }}"
      
      - name: Run tests
        run: npm test
Day 15-17: JavaScript Action
File: .github/actions/hello-action/action.yml

name: 'Hello Action'
description: 'A simple JavaScript action'

inputs:
  who-to-greet:
    description: 'Who to greet'
    required: true
    default: 'World'

outputs:
  time:
    description: 'The time we greeted you'

runs:
  using: 'node20'
  main: 'index.js'
File: .github/actions/hello-action/index.js

const core = require('@actions/core');
const github = require('@actions/github');

try {
  // Get input
  const nameToGreet = core.getInput('who-to-greet');
  console.log(`Hello ${nameToGreet}!`);
  
  // Get current time
  const time = new Date().toTimeString();
  
  // Set output
  core.setOutput('time', time);
  
  // Get context
  const payload = JSON.stringify(github.context.payload, undefined, 2);
  console.log(`The event payload: ${payload}`);
  
} catch (error) {
  core.setFailed(error.message);
}
File: .github/actions/hello-action/package.json

{
  "name": "hello-action",
  "version": "1.0.0",
  "description": "A simple GitHub Action",
  "main": "index.js",
  "scripts": {
    "test": "echo \"No tests yet\""
  },
  "dependencies": {
    "@actions/core": "^1.10.1",
    "@actions/github": "^6.0.0"
  }
}
Day 18-19: Deployment Workflow
File: .github/workflows/09-deploy-staging.yml

name: 09 - Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build application
        run: npm run build
        env:
          NODE_ENV: staging
          API_URL: ${{ secrets.STAGING_API_URL }}
      
      - name: Run tests
        run: npm test
      
      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment..."
          # Add your deployment commands here
          # Example: scp, rsync, or cloud provider CLI
        env:
          DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
      
      - name: Notify deployment
        if: success()
        run: echo "Deployment to staging successful!"
File: .github/workflows/10-deploy-production.yml

name: 10 - Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:  # Allow manual triggers

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build application
        run: npm run build
        env:
          NODE_ENV: production
      
      - name: Upload build
        uses: actions/upload-artifact@v4
        with:
          name: production-build
          path: dist/
  
  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    
    steps:
      - name: Download build
        uses: actions/download-artifact@v4
        with:
          name: production-build
          path: dist/
      
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Add production deployment commands
        env:
          DEPLOY_KEY: ${{ secrets.PRODUCTION_DEPLOY_KEY }}
      
      - name: Health check
        run: |
          echo "Running health check..."
          # curl https://example.com/health
      
      - name: Notify team
        if: success()
        run: echo "Production deployment successful!"
Day 18-19: GitHub Pages Deployment
File: .github/workflows/11-deploy-github-pages.yml

name: 11 - Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build site
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
Day 20-21: Reusable Workflow
File: .github/workflows/reusable-test.yml

name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        description: 'Node.js version'
        required: false
        type: string
        default: '20'
      run-lint:
        description: 'Whether to run linter'
        required: false
        type: boolean
        default: true
    outputs:
      test-result:
        description: 'Test result status'
        value: ${{ jobs.test.outputs.result }}
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      result: ${{ steps.test-step.outputs.result }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      
      - name: Install dependencies
        run: npm ci
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
      
      - name: Run linter
        if: inputs.run-lint
        run: npm run lint
      
      - name: Run tests
        id: test-step
        run: |
          npm test
          echo "result=success" >> $GITHUB_OUTPUT
File: .github/workflows/12-call-reusable-workflow.yml

name: 12 - Call Reusable Workflow

on: [push, pull_request]

jobs:
  call-test-workflow:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
      run-lint: true
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
  
  use-test-result:
    needs: call-test-workflow
    runs-on: ubuntu-latest
    steps:
      - name: Display test result
        run: echo "Test result was ${{ needs.call-test-workflow.outputs.test-result }}"
Day 20-21: Conditional Execution
File: .github/workflows/13-conditional-execution.yml

name: 13 - Conditional Execution

on: [push, pull_request]

jobs:
  conditional-steps:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Always runs
        run: echo "This always runs"
      
      - name: Only on main branch
        if: github.ref == 'refs/heads/main'
        run: echo "This runs only on main"
      
      - name: Only on pull requests
        if: github.event_name == 'pull_request'
        run: echo "This runs only on PRs"
      
      - name: Only when pushed by specific user
        if: github.actor == 'your-username'
        run: echo "This runs only for specific user"
      
      - name: Skip on draft PRs
        if: github.event.pull_request.draft == false
        run: echo "This skips draft PRs"
  
  conditional-jobs:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying to production"
  
  status-checks:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Might fail
        id: risky-step
        continue-on-error: true
        run: exit 1
      
      - name: Always runs after failure
        if: always()
        run: echo "This runs regardless of previous step status"
      
      - name: Only on success
        if: success()
        run: echo "Previous steps succeeded"
      
      - name: Only on failure
        if: failure()
        run: echo "Something failed"
      
      - name: Check specific step outcome
        if: steps.risky-step.outcome == 'failure'
        run: echo "The risky step failed"
Week 4: Optimization and Best Practices
Day 22-23: Advanced Caching
File: .github/workflows/14-advanced-caching.yml

name: 14 - Advanced Caching

on: [push]

jobs:
  cache-node:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'  # Built-in caching
      
      - name: Install dependencies
        run: npm ci
  
  multi-level-cache:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Cache node modules
        id: cache-npm
        uses: actions/cache@v4
        with:
          path: node_modules
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
      
      - name: Cache build output
        uses: actions/cache@v4
        with:
          path: |
            dist
            .next/cache
          key: ${{ runner.os }}-build-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-build-
      
      - name: Install dependencies
        if: steps.cache-npm.outputs.cache-hit != 'true'
        run: npm ci
      
      - name: Build
        run: npm run build
  
  restore-cache:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Restore cache
        uses: actions/cache/restore@v4
        with:
          path: node_modules
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      
      - name: Do work
        run: npm test
      
      - name: Save cache
        uses: actions/cache/save@v4
        if: always()
        with:
          path: node_modules
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
Day 24-25: Security Best Practices
File: .github/workflows/15-security-best-practices.yml

name: 15 - Security Best Practices

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Minimal permissions - grant only what's needed
permissions:
  contents: read

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      actions: read
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      # Pin actions to specific SHA for security
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@6e7b7d1fd3e4fef0c5fa8cce1229c54b2c9bd0d8  # v0.24.0
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
  
  dependency-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    permissions:
      contents: read
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
  
  codeql-analysis:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    
    strategy:
      matrix:
        language: ['javascript']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
      
      - name: Autobuild
        uses: github/codeql-action/autobuild@v3
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
  
  secret-scanning:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
Day 24-25: Secure Secrets Usage
File: .github/workflows/16-secure-secrets.yml

name: 16 - Secure Secrets Usage

on: [push]

# Minimal permissions
permissions:
  contents: read

jobs:
  use-secrets-safely:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      # Good: Use secrets in env, not directly in run
      - name: Use API key safely
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          # Never echo secrets!
          # This is safe - checks if set without exposing value
          if [ -z "$API_KEY" ]; then
            echo "API_KEY is not set"
            exit 1
          fi
          echo "API_KEY is configured"
      
      # Good: Pass secrets to actions via with/env
      - name: Deploy with credentials
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Use secrets in deployment commands
          echo "Deploying with authenticated access"
      
      # Bad example (commented out):
      # - name: DON'T DO THIS
      #   run: echo "Secret is ${{ secrets.MY_SECRET }}"
      
      # Good: Mask additional sensitive values
      - name: Mask custom values
        run: |
          sensitive_value="my-sensitive-data"
          echo "::add-mask::$sensitive_value"
          echo "Value is set: $sensitive_value"
  
  environment-secrets:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Use environment-specific secrets
        env:
          PROD_API_KEY: ${{ secrets.PROD_API_KEY }}
        run: echo "Using production API key"
Day 26-27: Monitoring and Debugging
File: .github/workflows/17-debugging.yml

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
