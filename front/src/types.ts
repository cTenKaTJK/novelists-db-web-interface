export interface Writer {
  id_писателя: number
  фамилия: string
  имя: string
  отчество?: string | null
  год_рождения?: number | null
  год_смерти?: number | null
  id_страны_рождения?: number | null
}

export interface Work {
  id_произведения: number
  название_произведения: string
  год_написания?: number | null
  id_жанра?: number | null
  genre?: { id_жанра: number; жанр: string } | null
}

export interface EditionStat {
  year: number
  total_circulation: number
}

export interface PopularAuthor {
  id: number
  фамилия: string
  имя: string
  total_circulation: number
}