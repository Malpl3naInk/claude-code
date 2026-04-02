// Stub for self-hosted runner
// This module is guarded by feature('SELF_HOSTED_RUNNER') which returns false
export async function selfHostedRunnerMain(_args: string[]): Promise<void> {
  throw new Error('Self-hosted runner feature is not available in this build');
}
