import { get } from './client'
import type { PopularAuthor } from '../types'

export const getPopularAuthors = (limit: number = 5) => get<PopularAuthor[]>(`/authors/popular?limit=${limit}`)