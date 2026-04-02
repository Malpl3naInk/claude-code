// Stub for server/lockfile
export function acquireLockfile(): boolean {
  return false;
}
export function releaseLockfile(): void {
  // No-op
}
export default { acquireLockfile, releaseLockfile };
