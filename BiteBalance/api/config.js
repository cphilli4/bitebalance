const getEnvVariables = (variableName) => {
  const envVar = process.env[`EXPO_PUBLIC_${variableName}`]
  if (envVar) {
    return envVar
  }
}

export const BACKEND_URL = getEnvVariables("BACKEND_URL")
export const BACKEND_PORT = getEnvVariables("BACKEND_URL_PORT")