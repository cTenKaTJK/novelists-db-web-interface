<script setup lang="ts">
import { ref, onMounted } from 'vue'

const stats = ref([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const res = await fetch('/api/editions/statistics')
    const data = await res.json()
    stats.value = data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div>
    <h2>Суммарный тираж по годам</h2>
    <table v-if="!loading">
      <thead><tr><th>Год</th><th>Тираж</th></tr></thead>
      <tbody>
        <tr v-for="s in stats" :key="s.year">
          <td>{{ s.year }}</td>
          <td>{{ s.total_circulation }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>Загрузка...</div>
  </div>
</template>