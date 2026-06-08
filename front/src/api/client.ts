const API_BASE = '/api'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const fullUrl = `${API_BASE}${url}`
  console.log('🔵 Запрос:', fullUrl, options?.method || 'GET')
  const response = await fetch(fullUrl, options)
  console.log('🟢 Ответ:', response.status, response.statusText)
  if (!response.ok) {
    const error = await response.text()
    console.error('🔴 Ошибка:', error)
    throw new Error(error || 'Ошибка запроса')
  }
  // Если статус 204 No Content, возвращаем пустой объект (или null)
  if (response.status === 204) {
    return null as T
  }
  // Если есть тело, парсим JSON
  const contentType = response.headers.get('content-type')
  if (contentType && contentType.includes('application/json')) {
    return response.json() as Promise<T>
  }
  return null as T
}

export const get = <T>(url: string) => request<T>(url)
export const post = <T>(url: string, body: unknown) =>
  request<T>(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
export const put = <T>(url: string, body: unknown) =>
  request<T>(url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
export const del = (url: string) => request<void>(url, { method: 'DELETE' })