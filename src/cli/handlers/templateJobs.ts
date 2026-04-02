// Stub for template jobs handler
// This module is guarded by feature('TEMPLATES') which returns false
export async function templatesMain(_args: string[]): Promise<void> {
  throw new Error('Templates feature is not available in this build');
}
