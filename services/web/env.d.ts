// Support for reading environment variablres
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      CRAPI_APP_NAME: string;
      // ... other environment variables
    }
  }
}

export {};
