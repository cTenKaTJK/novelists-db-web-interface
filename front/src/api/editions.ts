import { get, post } from './client'
import type { EditionStat } from '../types'

export const getEditionStatistics = () => get<EditionStat[]>('/editions/statistics')

export const createEdition = (data: {
  id_произведения: number
  страна_где_издавалось: number
  год_издания: number
  тираж_издания: number
  издательство?: string | null
}) => post('/editions', data)