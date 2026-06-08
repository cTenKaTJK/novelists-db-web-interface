import { get } from './client'

export const getCountries = () => get<{ id_страны: number; название_страны: string }[]>('/countries')