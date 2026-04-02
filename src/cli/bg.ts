// Stub for background session management
// This module is guarded by feature('BG_SESSIONS') which returns false
export async function psHandler(_args: string[]): Promise<void> {
  throw new Error('Background sessions feature is not available in this build');
}

export async function logsHandler(_id: string): Promise<void> {
  throw new Error('Background sessions feature is not available in this build');
}

export async function attachHandler(_id: string): Promise<void> {
  throw new Error('Background sessions feature is not available in this build');
}

export async function killHandler(_id: string): Promise<void> {
  throw new Error('Background sessions feature is not available in this build');
}

export async function handleBgFlag(_args: string[]): Promise<void> {
  throw new Error('Background sessions feature is not available in this build');
}
