<template>
  <div>
    <h2>Список писателей</h2>
    <ul v-if="!loading">
      <li v-for="w in writers" :key="w.id_писателя">
        {{ w.фамилия }} {{ w.имя }}
        <button @click="$emit('edit', w)">✏️</button>
        <button @click="$emit('delete', w.id_писателя)">🗑️</button>
      </li>
    </ul>
    <div v-else>Загрузка...</div>
  </div>
</template>

<script setup lang="ts">
import type { Writer } from '../../types'

defineProps<{ writers: Writer[]; loading: boolean }>()
defineEmits<{ (e: 'edit', writer: Writer): void; (e: 'delete', id: number): void }>()
</script>