<template>
  <div>
    <ul v-if="!loading" class="list">
      <li v-for="w in works" :key="w.id_произведения" class="list-item">
        <div>
          <strong>{{ w.название_произведения }}</strong>
          <span class="text-sm text-gray-500 block">— {{ w.genre?.жанр || 'без жанра' }}</span>
        </div>
        <div class="list-actions">
          <button @click="$emit('delete', w.id_произведения)" title="Удалить">🗑️</button>
        </div>
      </li>
    </ul>
    <div v-else class="text-center py-4">Загрузка...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { getWorks } from '../../api/works'
import type { Work } from '../../types'

const props = defineProps<{ authorId?: number; genreId?: number }>()
defineEmits<{ (e: 'delete', id: number): void }>()

const works = ref<Work[]>([])
const loading = ref(false)

async function loadWorks() {
  loading.value = true
  try {
    works.value = await getWorks(props.authorId, props.genreId)
  } finally {
    loading.value = false
  }
}

watch(() => [props.authorId, props.genreId], () => loadWorks(), { immediate: true })
onMounted(loadWorks)
</script>