import { get, post, put, del } from './client'
import type { Writer, PopularAuthor } from '../types'

export const getWriters = () => get<Writer[]>('/writers')
export const getWriter = (id: number) => get<Writer>(`/writers/${id}`)
export const createWriter = (data: Omit<Writer, 'id_писателя'>) => post<Writer>('/writers', data)
export const updateWriter = (id: number, data: Partial<Writer>) => put<Writer>(`/writers/${id}`, data)
export const deleteWriter = (id: number) => {
  console.log('🗑️ deleteWriter вызван с id:', id)
  return del(`/writers/${id}`)
}

export const getPopularAuthors = (limit: number = 5) => get<PopularAuthor[]>(`/authors/popular?limit=${limit}`)