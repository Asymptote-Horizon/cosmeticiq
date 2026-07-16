export function getErrorMessage(err: any): string {
  if (!err) return 'An unknown error occurred';
  
  const detail = err.response?.data?.detail;
  
  if (!detail) return err.message || 'An unknown error occurred';
  
  if (typeof detail === 'string') return detail;
  
  if (Array.isArray(detail)) {
    return detail.map((d: any) => d.msg || String(d)).join(', ');
  }
  
  if (typeof detail === 'object') {
    if (detail.msg) return String(detail.msg);
    if (detail.detail) return getErrorMessage({ response: { data: { detail: detail.detail } } });
    return JSON.stringify(detail);
  }
  
  return String(detail);
}
