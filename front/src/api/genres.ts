import { get } from './client'

export const getGenres = () => get<{ id_жанра: number; жанр: string }[]>('/genres')