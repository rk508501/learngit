# Node.js Deep Dive Reference Notes

## Table of Contents
1. [What Happens: `npx playwright test tests/abc.spec.ts`](#playwright-execution)
2. [What Happens: `node test.js`](#node-execution)
3. [Understanding `process.env`](#process-env)

---

## What Happens: `npx playwright test tests/abc.spec.ts` {#playwright-execution}

### 1. npx Resolution
`npx` (part of npm) first looks for the `playwright` executable in your local `node_modules/.bin/` directory. If it's not found there, it would download a temporary version, but in a Playwright project, it's typically already installed locally.

### 2. Playwright CLI Initialization
The Playwright CLI (`@playwright/test/cli`) starts up and parses your command-line arguments. It identifies that you want to run a specific test file: `tests/abc.spec.ts`.

### 3. Configuration Loading
Playwright searches for and loads your configuration file (usually `playwright.config.ts` or `playwright.config.js`) from the current directory or parent directories. This config contains:
- Browser types to use (Chromium, Firefox, WebKit)
- Base URL, timeouts, retries
- Reporter configurations
- Project settings (different browser configurations, devices)
- Global setup/teardown scripts

### 4. Test Discovery and Compilation
- Playwright uses its test runner to discover test files matching your pattern
- Since you're using TypeScript, it compiles `abc.spec.ts` on-the-fly using `esbuild` (fast) or `ts-node` depending on your setup
- It parses the test file to identify all `test()` blocks, `describe()` groups, hooks (`beforeEach`, `afterEach`, etc.)

### 5. Test Filtering
Based on your config's `projects` array, Playwright determines which browser/device combinations should run these tests. If you have multiple projects defined (e.g., chromium, firefox, mobile), it creates separate test runs for each.

### 6. Worker Pool Creation
Playwright spawns worker processes based on your `workers` config setting (defaults to half your CPU cores). Each worker is an isolated Node.js process that can run tests in parallel.

### 7. Browser Launch
For each project/browser type:
- Playwright downloads browser binaries if not already present (stored in `~/.cache/ms-playwright/`)
- Launches browser instances (can be headed or headless based on config)
- Creates browser contexts (isolated browser sessions with separate cookies, cache, etc.)

### 8. Test Execution
For each test in your spec file:
- A worker picks up the test from the queue
- Runs any `beforeAll`/`beforeEach` hooks
- Executes the test code with a fresh `page` object
- Captures screenshots/videos if configured
- Runs `afterEach`/`afterAll` hooks
- Handles retries on failure if configured

### 9. Tracing and Artifacts
During execution, Playwright can record:
- Screenshots on failure
- Video recordings
- Network activity
- Console logs
- Trace files (detailed timeline of all actions)

### 10. Reporting
As tests complete, results are sent to configured reporters (HTML, JSON, JUnit, etc.). The default reporter shows progress in your terminal with colored output indicating passes/failures.

### 11. Cleanup
After all tests finish:
- Browser contexts and instances are closed
- Worker processes terminate
- Final report is generated
- Exit code is set (0 for success, 1 for failures)

---

## Node.js Components Out of the Box

### Core Components Included with Node.js

When you install Node.js, you automatically get:

#### 1. Node.js Runtime
- The V8 JavaScript engine (from Chrome) that executes your JavaScript code
- Core built-in modules like `fs`, `http`, `path`, `crypto`, etc.
- The event loop and asynchronous I/O system

#### 2. npm (Node Package Manager)
- Automatically bundled with Node.js since version 0.6.3 (2011)
- A CLI tool for installing, managing, and publishing packages
- Access to the npm registry (npmjs.com) with millions of packages
- Located alongside node binary (e.g., `/usr/local/bin/npm`)

#### 3. npx (Node Package Execute)
- Bundled with npm since version 5.2.0 (July 2017)
- Comes automatically when you install Node.js (because npm comes with Node.js)
- It's essentially a wrapper/helper tool that ships as part of the npm package

### What npx Actually Does

**1. Execute local binaries without typing the full path:**
```bash
# Instead of:
./node_modules/.bin/playwright test

# You can use:
npx playwright test
```

**2. Run packages without installing them globally:**
```bash
# Runs create-react-app without installing it globally
npx create-react-app my-app
```

**3. Run specific versions of packages:**
```bash
npx playwright@1.40.0 test
```

### How to Check What You Have

```bash
# Check Node.js version
node --version  # e.g., v20.10.0

# Check npm version (comes with Node.js)
npm --version   # e.g., 10.2.3

# Check npx version (comes with npm)
npx --version   # same as npm version

# See where they're installed
which node      # e.g., /usr/local/bin/node
which npm       # e.g., /usr/local/bin/npm
which npx       # e.g., /usr/local/bin/npx
```

### The Relationship

```
Node.js Installation
├── node (runtime)
├── npm (package manager)
│   └── npx (package executor - part of npm)
└── Built-in modules (fs, http, etc.)
```

### What's NOT Included

These require separate installation:
- **yarn** - Alternative package manager (must install separately)
- **pnpm** - Another package manager (must install separately)
- **TypeScript** - Must install via `npm install -g typescript`
- **Any testing frameworks** - Playwright, Jest, etc. (install via npm)
- **Any third-party packages** - Express, React, etc. (install via npm)

### Historical Context

- **Pre-2011**: Node.js had no package manager
- **2011**: npm became bundled with Node.js
- **2017**: npx was added to npm, so it became available automatically
- **Today**: When you download Node.js from nodejs.org, you get node + npm + npx in one installer

---

## What Happens: `node test.js` {#node-execution}

### 1. Command Parsing
The shell (bash, zsh, PowerShell, etc.) parses your command and identifies:
- `node` - the executable to run
- `test.js` - the argument (file path) to pass to node

### 2. Node Binary Lookup
Your shell searches for the `node` executable in directories listed in your `PATH` environment variable:
```bash
# Typically found at:
# macOS/Linux: /usr/local/bin/node or /usr/bin/node
# Windows: C:\Program Files\nodejs\node.exe
```

### 3. Node.js Process Initialization
Once the node binary is found and executed:

**a) Process Creation:**
- A new operating system process is spawned
- Process gets a unique PID (process ID)
- Memory is allocated for the Node.js runtime

**b) V8 Engine Initialization:**
- V8 JavaScript engine (Google's JIT compiler) starts up
- Heap memory is allocated for objects
- Call stack is initialized
- Garbage collector is set up

**c) libuv Initialization:**
- libuv (cross-platform async I/O library) starts
- Event loop is created
- Thread pool is initialized (default 4 threads for file I/O, DNS, etc.)

### 4. File Reading
Node.js reads `test.js` from your file system:
- Uses the `fs` module internally
- Reads the file as UTF-8 text (default)
- If file doesn't exist, throws `Error: Cannot find module`

### 5. Code Compilation
The JavaScript code goes through V8's compilation pipeline:

**a) Parsing:**
- V8 parses your JavaScript into an Abstract Syntax Tree (AST)
- Syntax errors are caught here

**b) Compilation:**
- AST is converted to bytecode by V8's Ignition interpreter
- Hot code paths may be optimized to machine code by TurboFan (JIT compiler)

**c) Module Wrapping:**
Your code is wrapped in a function wrapper:
```javascript
(function(exports, require, module, __filename, __dirname) {
    // Your test.js code goes here
});
```
This is why you have access to `require`, `module`, `__filename`, `__dirname` without importing them.

### 6. Execution Context Setup
Node.js creates the execution context:
- Global object is created
- Global variables like `console`, `process`, `Buffer`, `setTimeout` are attached
- `require` function is made available
- `module` and `exports` objects are created

### 7. Code Execution
Your JavaScript code runs top-to-bottom:

**Synchronous Code:**
```javascript
console.log('Hello'); // Executes immediately
const x = 5 + 3;      // Calculated immediately
```

**Asynchronous Code:**
```javascript
setTimeout(() => {
    console.log('Later');
}, 1000);

fs.readFile('data.txt', (err, data) => {
    console.log(data);
});
```
- Async operations are registered with libuv
- Callbacks are queued for later execution
- Event loop continues

### 8. Event Loop Processing
This is the heart of Node.js asynchronous execution:

```
   ┌───────────────────────────┐
┌─>│           timers          │  setTimeout/setInterval callbacks
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │  I/O callbacks deferred from previous loop
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │  Internal use
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           poll            │  Retrieve new I/O events
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           check           │  setImmediate callbacks
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │      close callbacks      │  socket.on('close', ...)
│  └───────────────────────────┘
└──────────────────────────────────
```

The event loop keeps running until:
- No more pending operations
- No more timers
- No more callbacks to execute

### 9. Module Loading (if using require)
If your test.js contains `require()`:

```javascript
const express = require('express');
```

**Module Resolution:**
1. Check if it's a core module (fs, http, path, etc.) - load directly
2. If not core, look for `node_modules/express/`
3. Read `package.json` to find entry point
4. Load and cache the module

**Module Caching:**
- First `require('express')` loads and executes the module
- Subsequent `require('express')` returns cached version
- Cache stored in `require.cache`

### 10. Built-in APIs Available
Your code has access to Node.js APIs without importing:

**Global objects:**
- `console` - for logging
- `process` - process info, exit codes, env variables
- `Buffer` - binary data handling
- `global` - global namespace
- Timers: `setTimeout`, `setInterval`, `setImmediate`

**Available via require:**
```javascript
const fs = require('fs');        // File system
const http = require('http');    // HTTP server/client
const path = require('path');    // Path utilities
const crypto = require('crypto'); // Cryptography
```

### 11. Error Handling
If errors occur:

**Uncaught Exceptions:**
```javascript
throw new Error('Oops');
// Process crashes with stack trace
```

**Unhandled Promise Rejections:**
```javascript
Promise.reject('Failed');
// Node.js 15+: process terminates
// Earlier: warning printed
```

**Handled Errors:**
```javascript
try {
    throw new Error('Caught');
} catch(e) {
    console.error(e);
}
// Process continues
```

### 12. Process Exit
Node.js process exits when:

**a) Normal Exit:**
- All synchronous code executed
- Event loop has no more work (no pending callbacks, timers, or I/O)
- Exit code: 0 (success)

**b) Explicit Exit:**
```javascript
process.exit(0);  // Success
process.exit(1);  // Error
```

**c) Uncaught Exception:**
- Exit code: 1 (error)
- Stack trace printed to stderr

### 13. Cleanup
Before termination:
- `process.on('exit')` handlers run
- Resources are freed
- File descriptors closed
- Memory released back to OS

### Simple Example Flow

For this `test.js`:
```javascript
console.log('Start');

setTimeout(() => {
    console.log('Timeout');
}, 0);

Promise.resolve().then(() => {
    console.log('Promise');
});

console.log('End');
```

**Execution order:**
1. `Start` - synchronous
2. `End` - synchronous
3. `Promise` - microtask queue (higher priority)
4. `Timeout` - timer queue (lower priority)

### Key Differences from Browser

- No `window` or `document` objects
- Has `process`, `Buffer`, `require`
- Different global scope (`global` vs `window`)
- Access to file system and OS operations
- Single-threaded event loop (but with worker threads available)

---

## Understanding `process.env` {#process-env}

### What `process.env` Really Is

`process.env` is **not** a plain JSON object, and `env` is **not** a property attached to the global object.

### 1. `process` is the Parent Object

`process` is a **global object** (not attached to `global`, but available globally):
- It's a special built-in object provided by Node.js
- Available everywhere without requiring it
- Contains information about the current Node.js process

```javascript
console.log(typeof process);        // 'object'
console.log(process.pid);           // Process ID (e.g., 12345)
console.log(process.version);       // Node version (e.g., 'v20.10.0')
console.log(process.platform);      // OS platform (e.g., 'linux', 'darwin', 'win32')
```

### 2. `env` is a Property of `process`

`process.env` is a property that contains **environment variables**:

```javascript
// Access environment variables
console.log(process.env.PATH);      // Your system PATH
console.log(process.env.HOME);      // Home directory (Unix/Mac)
console.log(process.env.USERPROFILE); // Home directory (Windows)
console.log(process.env.NODE_ENV);  // Often 'development' or 'production'
```

### 3. What Type of Object is `process.env`?

It's a **special object**, not a plain JavaScript object or JSON:

```javascript
console.log(typeof process.env);              // 'object'
console.log(process.env instanceof Object);   // true
console.log(JSON.stringify(process.env));     // Works, but...

// It's not a plain object:
console.log(Object.getPrototypeOf(process.env)); // Not Object.prototype
```

**Key characteristics:**
- All values are **strings** (environment variables are always strings in the OS)
- It's a **live object** - changes reflect immediately
- Reading non-existent properties returns `undefined`

### 4. Where Does `process.env` Come From?

Environment variables come from your operating system:

**From your shell:**
```bash
# Set environment variable in terminal
export MY_VAR="hello"
node test.js

# Or inline
MY_VAR="hello" node test.js
```

**In your Node.js code:**
```javascript
// test.js
console.log(process.env.MY_VAR); // 'hello'
```

**From .env files (with libraries like dotenv):**
```bash
# .env file
DATABASE_URL=postgres://localhost/mydb
API_KEY=secret123
```

```javascript
// Load .env into process.env
require('dotenv').config();

console.log(process.env.DATABASE_URL); // 'postgres://localhost/mydb'
console.log(process.env.API_KEY);      // 'secret123'
```

### 5. Important: All Values Are Strings

```javascript
// Set in terminal: PORT=3000 node test.js

console.log(process.env.PORT);           // '3000' (string, not number!)
console.log(typeof process.env.PORT);    // 'string'

// Need to convert:
const port = parseInt(process.env.PORT, 10);  // 3000 (number)
const port = Number(process.env.PORT);        // 3000 (number)

// Boolean values also come as strings:
// IS_PROD=true node test.js
console.log(process.env.IS_PROD);        // 'true' (string!)
console.log(process.env.IS_PROD === true); // false
console.log(process.env.IS_PROD === 'true'); // true
```

### 6. You Can Modify `process.env`

```javascript
// Add new environment variable at runtime
process.env.MY_NEW_VAR = 'value';
console.log(process.env.MY_NEW_VAR); // 'value'

// Modify existing
process.env.NODE_ENV = 'production';

// Delete
delete process.env.MY_NEW_VAR;
console.log(process.env.MY_NEW_VAR); // undefined
```

**Note:** Changes only affect the current Node.js process and its child processes, not your shell or other processes.

### 7. Common Environment Variables

Node.js and tools often use these:

```javascript
process.env.NODE_ENV          // 'development', 'production', 'test'
process.env.PATH              // System PATH for executables
process.env.HOME              // User home directory (Unix/Mac)
process.env.USERPROFILE       // User home directory (Windows)
process.env.PWD               // Current working directory
process.env.USER              // Current username
process.env.LANG              // System language/locale
```

### 8. Relationship to Global Object

To clarify the hierarchy:

```javascript
// These are global (available everywhere):
console.log(process);           // ✅ Available
console.log(__dirname);         // ✅ Available
console.log(require);           // ✅ Available

// But they're NOT properties of 'global':
console.log(global.process);    // ✅ Also available (same object)
console.log(global.__dirname);  // ❌ undefined
console.log(global.require);    // ❌ undefined

// Only variables you create without 'var/let/const' go on global:
myVar = 'test';
console.log(global.myVar);      // 'test'
```

### Visual Summary

```
Operating System Environment Variables
           ↓
    Node.js Process Starts
           ↓
   process.env is populated
           ↓
Your code accesses process.env.VARIABLE_NAME
           ↓
  Returns string value or undefined
```

### Practical Example for Testing

```javascript
// Set different configs based on environment
const config = {
  development: {
    apiUrl: 'http://localhost:3000',
    debug: true
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false
  }
};

// Get current environment (defaults to 'development')
const env = process.env.NODE_ENV || 'development';
const currentConfig = config[env];

console.log(`Running in ${env} mode`);
console.log(`API URL: ${currentConfig.apiUrl}`);
```

### Key Takeaway

**`process.env` is a special object property of the global `process` object, not a JSON attached to the global object. It contains environment variables from your OS as string key-value pairs.**

---

## Summary

- **npx**: Part of npm, executes packages from local or remote sources
- **node test.js**: Spawns V8 process, compiles code, runs event loop, executes your JavaScript
- **process.env**: Special object containing OS environment variables as strings
