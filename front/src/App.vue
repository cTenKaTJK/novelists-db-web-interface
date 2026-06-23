<template>
  <div class="container">
    <h1 class="page-title">База книг</h1>

    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Вкладки -->
    <div class="tab-content">
      <!-- Писатели -->
      <div v-if="activeTab === 'writers'" class="tab-pane">
        <div class="card">
          <div class="card-title">Добавить / редактировать писателя</div>
          <WriterForm :initial="editingWriter" :countries="countries" @submit="saveWriter" />
          <hr />
          <WriterList :writers="writers" :loading="loadingWriters" @edit="editWriter" @delete="handleDeleteWriter" />
        </div>
      </div>

      <!-- Произведения -->
      <div v-if="activeTab === 'works'" class="tab-pane">
        <div class="card">
          <div class="card-title">Произведения</div>
          <div class="filter-row">
            <div class="form-group">
              <select v-model="selectedAuthorId">
                <option :value="undefined">Все авторы</option>
                <option v-for="w in writers" :key="w.id_писателя" :value="w.id_писателя">
                  {{ w.фамилия }} {{ w.имя }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <select v-model="selectedGenreId">
                <option :value="undefined">Все жанры</option>
                <option v-for="g in genres" :key="g.id_жанра" :value="g.id_жанра">
                  {{ g.жанр }}
                </option>
              </select>
            </div>
          </div>
          <WorkList :author-id="selectedAuthorId" :genre-id="selectedGenreId" :key="refreshWorksKey" @delete="handleDeleteWork"/>
          <AddWork :writers="writers" :genres="genres" @added="onWorkAdded" />
        </div>
      </div>

      <div v-if="activeTab === 'editions'" class="tab-pane">
        <AddEdition :works="worksForSelect" :countries="countries" @added="onEditionAdded" />
      </div>

      <!-- Статистика -->
      <div v-if="activeTab === 'stats'" class="tab-pane">
        <div class="grid-2cols">
          <div class="card">
            <div class="card-title">Популярные писатели</div>
            <PopularAuthors />
          </div>
          <div class="card">
            <div class="card-title">Тираж по годам</div>
            <EditionStatistics />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import WriterList from './components/writers/WriterList.vue'
import WriterForm from './components/writers/WriterForm.vue'
import WorkList from './components/works/WorkList.vue'
import AddWork from './components/works/AddWork.vue'
import EditionStatistics from './components/editions/EditionStatistics.vue'
import PopularAuthors from './components/writers/PopularWriters.vue'
import AddEdition from './components/editions/AddEdition.vue'
import { getWriters, createWriter, updateWriter, deleteWriter as deleteWriterApi } from './api/writers'
import { getWorks, deleteWork } from './api/works'
import { getGenres } from './api/genres'
import { getCountries } from './api/countries'
import type { Writer } from './types'

// Состояние вкладок
const tabs = [
  { key: 'writers', label: 'Писатели' },
  { key: 'works', label: 'Произведения' },
  { key: 'editions', label: 'Издания' },
  { key: 'stats', label: 'Статистика' },
]
const activeTab = ref('writers')

// Данные писателей
const writers = ref<Writer[]>([])
const loadingWriters = ref(false)
const editingWriter = ref<Writer | null>(null)

// Данные для фильтрации произведений
const genres = ref<{ id_жанра: number; жанр: string }[]>([])
const selectedAuthorId = ref<number | undefined>(undefined)
const selectedGenreId = ref<number | undefined>(undefined)

const worksForSelect = ref<{ id_произведения: number; название_произведения: string }[]>([])
const countries = ref<{ id_страны: number; название_страны: string }[]>([])

const refreshWorksKey = ref(0)

// Добавление нового произведения
function onWorkAdded() {
  refreshWorksKey.value++
}

async function loadWorksForSelect() {
  try {
    const works = await getWorks()
    worksForSelect.value = works.map(w => ({ id_произведения: w.id_произведения, название_произведения: w.название_произведения }))
  } catch (err) { console.error(err) }
}

async function loadCountries() {
  try {
    countries.value = await getCountries()
  } catch (err) {
    console.error(err)
  }
}

function onEditionAdded() {
  // пока просто заглушка (позже можно обновить список изданий)
  console.log('Издание добавлено')
}

// Удаление произведения
async function handleDeleteWork(id: number) {
  if (!confirm('Удалить произведение?')) return
  try {
    await deleteWork(id)
    refreshWorksKey.value++   // принудительно перезагрузить список
  } catch (err) {
    console.error('Ошибка удаления:', err)
  }
}

// Загрузка списка писателей
async function loadWriters() {
  loadingWriters.value = true
  try {
    writers.value = await getWriters()
  } finally {
    loadingWriters.value = false
  }
}

// Загрузка жанров
async function loadGenres() {
  try {
    genres.value = await getGenres()
  } catch (err) {
    console.error(err)
  }
}

// Сохранение писателя (добавление / редактирование)
async function saveWriter(data: Omit<Writer, 'id_писателя'>) {
  try {
    if (editingWriter.value) {
      const updated = await updateWriter(editingWriter.value.id_писателя, data)
      const idx = writers.value.findIndex(w => w.id_писателя === updated.id_писателя)
      if (idx !== -1) writers.value[idx] = updated
      editingWriter.value = null
    } else {
      const created = await createWriter(data)
      writers.value.push(created)
    }
  } catch (err) {
    console.error('Ошибка сохранения:', err)
  }
}

function editWriter(writer: Writer) {
  editingWriter.value = writer
}

async function handleDeleteWriter(id: number) {
  if (!confirm('Удалить писателя?')) return
  try {
    await deleteWriterApi(id)
    writers.value = writers.value.filter(w => w.id_писателя !== id)
  } catch (err) {
    console.error('Ошибка удаления:', err)
  }
}

onMounted(() => {
  loadWorksForSelect()
  loadCountries()
  loadWriters()
  loadGenres()
})
</script>

<style scoped>
/* Дополнительные стили для вкладок */
.tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 1.5rem;
}
.tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 0.5rem 0.5rem 0 0;
}
.tab-btn.active {
  color: #3b82f6;
  background-color: #eff6ff;
  border-bottom: 2px solid #3b82f6;
  margin-bottom: -2px;
}
.tab-btn:hover:not(.active) {
  background-color: #f1f5f9;
}
.tab-pane {
  animation: fade 0.2s ease;
}
@keyframes fade {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>