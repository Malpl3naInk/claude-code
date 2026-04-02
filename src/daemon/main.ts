// Stub for daemon main
// This module is guarded by feature('DAEMON') which returns false
export async function daemonMain(_args: string[]): Promise<void> {
  throw new Error('Daemon feature is not available in this build');
}
