<template>
  <div>
    <h2>Топ авторов по тиражу</h2>
    <ol v-if="!loading">
      <li v-for="a in authors" :key="a.id">
        {{ a.фамилия }} {{ a.имя }} — тираж: {{ a.total_circulation }}
      </li>
    </ol>
    <div v-else>Загрузка...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getPopularAuthors } from '../../api/writers'
import type { PopularAuthor } from '../../types'

const authors = ref<PopularAuthor[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    authors.value = await getPopularAuthors(5)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>