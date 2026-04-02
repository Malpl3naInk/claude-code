// Stub for environment runner
// This module is guarded by feature('BYOC_ENVIRONMENT_RUNNER') which returns false
export async function environmentRunnerMain(_args: string[]): Promise<void> {
  throw new Error('Environment runner feature is not available in this build');
}
