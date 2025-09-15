# Playwright Environment Fixture - Cliff Notes

## The Code

```typescript
// fixtures/env.fixture.ts
import { test as base } from "@playwright/test";
import { loadEnvConfig } from "../utils/envLoader";

type EnvConfig = ReturnType<typeof loadEnvConfig>;

export const test = base.extend<{
  envConfig: EnvConfig;
  userName: string;
  apiClient: ApiClient;
}>({
  envConfig: async ({}, use) => {
    const config = loadEnvConfig();
    await use(config);
  },
  userName: async ({ envConfig }, use) => {
    await use(envConfig.defaultUser);
  },
  apiClient: async ({ envConfig }, use) => {
    const client = new ApiClient(envConfig.apiUrl);
    await use(client);
  },
});

export const expect = test.expect;
```

## Key Concepts

### 1. `ReturnType<typeof loadEnvConfig>`

- `typeof loadEnvConfig` → Gets the function type: `() => ConfigObject`
- `ReturnType<...>` → Extracts just the return type: `ConfigObject`
- **Why both?** `typeof` gives you the whole function, `ReturnType` extracts what it returns

### 2. `base.extend<Type>(implementation)`

```typescript
base.extend<{
  // ← Type definition (what fixtures)
  envConfig: EnvConfig;
  userName: string;
  apiClient: ApiClient;
}>({
  // ← Implementation (how to create them)
  envConfig: async ({}, use) => {
    const config = loadEnvConfig();
    await use(config);
  },
  userName: async ({ envConfig }, use) => {
    await use(envConfig.defaultUser);
  },
  apiClient: async ({ envConfig }, use) => {
    const client = new ApiClient(envConfig.apiUrl);
    await use(client);
  },
});
```

### 3. Fixture Function Pattern

```typescript
async (dependencies, use) => {
  const value = createSomething();
  await use(value); // Provides value to tests
};
```

## Usage Example

```typescript
import { test, expect } from "./fixtures/env.fixture";

test("my test", async ({ page, envConfig, userName, apiClient }) => {
  // envConfig, userName, apiClient automatically loaded and typed
  await page.goto(envConfig.baseUrl);
  console.log(userName); // default user from config
  await apiClient.doSomething();
});
```

## Benefits

- **DRY**: Config loaded once per test
- **Type Safety**: Full TypeScript support
- **Clean**: Import `test` and `expect` from one place
- **Automatic**: No manual config loading in tests
- **Composable**: Fixtures can depend on each other

## Quick Reference

| Syntax                       | Purpose                                |
| ---------------------------- | -------------------------------------- |
| `typeof func`                | Get function's type signature          |
| `ReturnType<T>`              | Extract return type from function type |
| `base.extend<{}>({})`        | Add custom fixtures to Playwright      |
| `async ({}, use) => {}`      | Fixture function signature             |
| `await use(value)`           | Provide fixture value to tests         |
| `async ({ dep }, use) => {}` | Fixture depending on another fixture   |

## Mental Model

Think of fixtures as "test dependencies" that are:

1. **Declared** in the type parameter `<{...}>`
2. **Implemented** in the object parameter `({...})`
3. **Injected** into test functions automatically
