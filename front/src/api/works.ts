import { get, post, del } from './client'
import type { Work } from '@/types'

export const getWorks = (authorId?: number, genreId?: number) => {
  const params = new URLSearchParams()
  if (authorId) params.append('author_id', String(authorId))
  if (genreId) params.append('genre_id', String(genreId))
  const query = params.toString() ? `?${params.toString()}` : ''
  const url = `/works${query}`
  console.log('getWorks URL:', url)
  return get<Work[]>(url)
}

export const createWork = (data: { 
  название_произведения: string
  автор_id: number
  id_жанра: number
  год_написания?: number | null 
}) => post<Work>('/works', data)

export const deleteWork = (id: number) => del(`/works/${id}`)