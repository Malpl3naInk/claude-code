// Stub for daemon worker registry
// This module is guarded by feature('DAEMON') which returns false
export async function runDaemonWorker(_kind: string): Promise<void> {
  throw new Error('Daemon feature is not available in this build');
}
